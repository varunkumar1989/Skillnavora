"""Reference maths for the 9/21 EMA crossover options strategy.

Pure Python, standard library only. It is NOT a trading system and it does not talk to any broker.
It implements the calculations the handbook describes so they can be checked by tests:
  - EMA, crossover detection on candle close
  - friction model: premium slippage, one-tick penalty per side, statutory charges
  - KPI scorecard: win rate, gross and net PnL, profit factor, payoff ratio, expectancy, max drawdown

Every rate in CHARGES is an ASSUMPTION to be confirmed against the broker's and the exchanges'
current published schedules before use. Nothing here is verified against live charges.
"""
from dataclasses import dataclass, field

# --- assumptions (confirm each one; the values are placeholders for the maths, not quotes) ---
CHARGES = {
    "brokerage_per_order": 20.0,        # flat INR per order [Check: broker plan]
    "stt_sell_premium_rate": 0.001,     # 0.10% of premium on sell side of options [Check: current Finance Act rate]
    "exchange_txn_rate": 0.0003503,     # 0.03503% of premium turnover [Check: exchange schedule]
    "sebi_fee_rate": 0.000001,          # INR 10 per crore = 0.0001% [Check]
    "stamp_duty_buy_rate": 0.00003,     # 0.003% on buy side [Check: intraday rule]
    "gst_rate": 0.18,                   # on brokerage + exchange + SEBI fees [Check]
}
SLIPPAGE_RATE = 0.005   # 0.5% adverse premium slippage on each fill (brief's assumption)
TICK = 0.05             # one tick (INR) adverse on each fill (brief's assumption)


def ema(values, period):
    """Exponential moving average, alpha = 2/(period+1), seeded with the first value.

    The seed choice affects the first ~3*period values; warm up before trusting a signal.
    """
    if period < 1:
        raise ValueError("period must be >= 1")
    if not values:
        return []
    alpha = 2.0 / (period + 1)
    out = [float(values[0])]
    for v in values[1:]:
        out.append(alpha * float(v) + (1 - alpha) * out[-1])
    return out


def crossovers(closes, fast=9, slow=21, warmup=None):
    """Return a list of (index, 'bull' | 'bear') for crosses confirmed on candle close.

    A bull cross at i: fast[i-1] <= slow[i-1] and fast[i] > slow[i].
    A bear cross at i: fast[i-1] >= slow[i-1] and fast[i] < slow[i].
    Signals before `warmup` bars (default: slow period) are ignored.
    """
    if warmup is None:
        warmup = slow
    f, s = ema(closes, fast), ema(closes, slow)
    signals = []
    for i in range(max(1, warmup), len(closes)):
        if f[i - 1] <= s[i - 1] and f[i] > s[i]:
            signals.append((i, "bull"))
        elif f[i - 1] >= s[i - 1] and f[i] < s[i]:
            signals.append((i, "bear"))
    return signals


def fill_price(premium, side):
    """Adverse fill: buys cost more, sells receive less. side is 'buy' or 'sell'."""
    if side == "buy":
        return premium * (1 + SLIPPAGE_RATE) + TICK
    if side == "sell":
        return max(0.0, premium * (1 - SLIPPAGE_RATE) - TICK)
    raise ValueError("side must be 'buy' or 'sell'")


def leg_charges(side, fill, qty, c=CHARGES):
    """Statutory and broker charges for one leg (one order). Returns a dict of INR amounts."""
    turnover = fill * qty
    brokerage = c["brokerage_per_order"]
    exchange = turnover * c["exchange_txn_rate"]
    sebi = turnover * c["sebi_fee_rate"]
    stt = turnover * c["stt_sell_premium_rate"] if side == "sell" else 0.0
    stamp = turnover * c["stamp_duty_buy_rate"] if side == "buy" else 0.0
    gst = (brokerage + exchange + sebi) * c["gst_rate"]
    total = brokerage + exchange + sebi + stt + stamp + gst
    return {"brokerage": brokerage, "exchange": exchange, "sebi": sebi, "stt": stt,
            "stamp": stamp, "gst": gst, "total": total}


def round_trip(entry_premium, exit_premium, qty, long_option=True):
    """Net PnL of one option trade with frictions.

    long_option=True  : buy at entry, sell at exit (ATM/ITM option buy).
    long_option=False : sell at entry, buy back at exit (ATM option sell).
    Returns a dict with gross, charges, net and the fill prices used.
    """
    if long_option:
        entry_side, exit_side = "buy", "sell"
        entry_fill = fill_price(entry_premium, "buy")
        exit_fill = fill_price(exit_premium, "sell")
        gross = (exit_premium - entry_premium) * qty
        frictions_price = (entry_fill - entry_premium + exit_premium - exit_fill) * qty
    else:
        entry_side, exit_side = "sell", "buy"
        entry_fill = fill_price(entry_premium, "sell")
        exit_fill = fill_price(exit_premium, "buy")
        gross = (entry_premium - exit_premium) * qty
        frictions_price = (entry_premium - entry_fill + exit_fill - exit_premium) * qty
    charges = (leg_charges(entry_side, entry_fill, qty)["total"]
               + leg_charges(exit_side, exit_fill, qty)["total"])
    net = gross - frictions_price - charges
    return {"gross": round(gross, 2), "price_frictions": round(frictions_price, 2),
            "charges": round(charges, 2), "net": round(net, 2),
            "entry_fill": round(entry_fill, 4), "exit_fill": round(exit_fill, 4)}


@dataclass
class Scorecard:
    trades: int = 0
    wins: int = 0
    losses: int = 0
    win_rate_pct: float = 0.0
    gross: float = 0.0
    charges: float = 0.0
    net: float = 0.0
    profit_factor: float = 0.0
    payoff_ratio: float = 0.0
    expectancy: float = 0.0
    max_drawdown: float = 0.0
    notes: list = field(default_factory=list)


def scorecard(trades):
    """trades: list of dicts with keys gross, charges, net (INR). Returns a Scorecard."""
    sc = Scorecard()
    if not trades:
        sc.notes.append("no trades")
        return sc
    nets = [t["net"] for t in trades]
    sc.trades = len(trades)
    sc.wins = sum(1 for n in nets if n > 0)
    sc.losses = sum(1 for n in nets if n < 0)
    sc.win_rate_pct = round(100.0 * sc.wins / sc.trades, 2)
    sc.gross = round(sum(t["gross"] for t in trades), 2)
    sc.charges = round(sum(t["charges"] for t in trades), 2)
    sc.net = round(sum(nets), 2)
    gains = sum(n for n in nets if n > 0)
    losses = -sum(n for n in nets if n < 0)
    if losses == 0:
        sc.profit_factor = float("inf") if gains > 0 else 0.0
        sc.notes.append("no losing trades: profit factor is not meaningful")
    else:
        sc.profit_factor = round(gains / losses, 2)
    avg_win = (gains / sc.wins) if sc.wins else 0.0
    avg_loss = (losses / sc.losses) if sc.losses else 0.0
    sc.payoff_ratio = round(avg_win / avg_loss, 2) if avg_loss else float("inf") if avg_win else 0.0
    sc.expectancy = round(sc.net / sc.trades, 2)
    peak, equity, mdd = 0.0, 0.0, 0.0
    for n in nets:
        equity += n
        peak = max(peak, equity)
        mdd = max(mdd, peak - equity)
    sc.max_drawdown = round(mdd, 2)
    if sc.trades < 30:
        sc.notes.append(f"only {sc.trades} trades: results are too few to be statistically meaningful")
    return sc


def whipsaw_count(trades, max_bars=3):
    """Trades that lost and were closed within max_bars candles by a reverse crossover."""
    return sum(1 for t in trades
               if t.get("net", 0) < 0 and t.get("exit_reason") == "reverse_cross"
               and t.get("bars_held", 10**9) <= max_bars)
