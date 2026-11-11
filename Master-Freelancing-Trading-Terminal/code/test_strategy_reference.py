"""Tests for strategy_reference.py. Run: python3 test_strategy_reference.py"""
import math
import unittest
import strategy_reference as s


class EMATests(unittest.TestCase):
    def test_constant_series_stays_constant(self):
        self.assertTrue(all(abs(x - 100) < 1e-9 for x in s.ema([100] * 50, 9)))

    def test_first_value_is_seed(self):
        self.assertEqual(s.ema([10, 20], 9)[0], 10)

    def test_known_step(self):
        # alpha for period 3 is 0.5: 10 -> 0.5*20 + 0.5*10 = 15
        self.assertAlmostEqual(s.ema([10, 20], 3)[1], 15.0)

    def test_rejects_bad_period(self):
        with self.assertRaises(ValueError):
            s.ema([1, 2], 0)


class CrossoverTests(unittest.TestCase):
    def test_bull_and_bear_detected_on_close(self):
        up = [100.0] * 30 + [100 + 2 * i for i in range(1, 31)]
        down = [up[-1] - 2 * i for i in range(1, 41)]
        sig = s.crossovers(up + down, fast=9, slow=21)
        kinds = [k for _, k in sig]
        self.assertIn("bull", kinds)
        self.assertIn("bear", kinds)
        self.assertEqual(kinds[0], "bull")

    def test_flat_market_gives_no_signal(self):
        self.assertEqual(s.crossovers([100.0] * 100), [])

    def test_warmup_respected(self):
        closes = [100.0] * 5 + [110.0] * 5
        self.assertTrue(all(i >= 21 for i, _ in s.crossovers(closes, warmup=21)))


class FrictionTests(unittest.TestCase):
    def test_fill_prices(self):
        self.assertAlmostEqual(s.fill_price(100, "buy"), 100 * 1.005 + 0.05)
        self.assertAlmostEqual(s.fill_price(100, "sell"), 100 * 0.995 - 0.05)

    def test_sell_fill_never_negative(self):
        self.assertEqual(s.fill_price(0.01, "sell"), 0.0)

    def test_stt_only_on_sell_leg(self):
        buy = s.leg_charges("buy", 100, 75)
        sell = s.leg_charges("sell", 100, 75)
        self.assertEqual(buy["stt"], 0.0)
        self.assertAlmostEqual(sell["stt"], 100 * 75 * s.CHARGES["stt_sell_premium_rate"])
        self.assertEqual(sell["stamp"], 0.0)
        self.assertGreater(buy["stamp"], 0)

    def test_gst_on_brokerage_and_fees_only(self):
        leg = s.leg_charges("sell", 100, 75)
        base = leg["brokerage"] + leg["exchange"] + leg["sebi"]
        self.assertAlmostEqual(leg["gst"], base * 0.18)

    def test_round_trip_long_option_hand_check(self):
        # buy at 100, sell at 110, 75 units
        r = s.round_trip(100, 110, 75, long_option=True)
        self.assertEqual(r["gross"], 750.0)
        buy_fill = 100 * 1.005 + 0.05
        sell_fill = 110 * 0.995 - 0.05
        self.assertAlmostEqual(r["price_frictions"], (buy_fill - 100 + 110 - sell_fill) * 75, places=1)
        self.assertLess(r["net"], r["gross"])
        self.assertAlmostEqual(r["net"], r["gross"] - r["price_frictions"] - r["charges"], places=1)

    def test_round_trip_short_option_direction(self):
        r = s.round_trip(100, 90, 75, long_option=False)   # sold at 100, bought back at 90: profit
        self.assertEqual(r["gross"], 750.0)
        self.assertGreater(r["net"], 0)

    def test_losing_trade_is_negative_after_frictions(self):
        r = s.round_trip(100, 100, 75, long_option=True)   # flat price move still loses
        self.assertLess(r["net"], 0)


class ScorecardTests(unittest.TestCase):
    def test_basic_kpis(self):
        trades = [{"gross": 300, "charges": 20, "net": 280},
                  {"gross": -100, "charges": 20, "net": -120},
                  {"gross": 200, "charges": 20, "net": 180}]
        sc = s.scorecard(trades)
        self.assertEqual(sc.trades, 3)
        self.assertEqual(sc.wins, 2)
        self.assertEqual(sc.losses, 1)
        self.assertAlmostEqual(sc.win_rate_pct, 66.67, places=2)
        self.assertEqual(sc.net, 340)
        self.assertAlmostEqual(sc.profit_factor, 460 / 120, places=2)
        self.assertAlmostEqual(sc.expectancy, 340 / 3, places=2)
        self.assertEqual(sc.max_drawdown, 120)   # equity 280 -> 160 after the loss

    def test_max_drawdown(self):
        trades = [{"gross": 0, "charges": 0, "net": n} for n in (100, -150, 50, -200, 300)]
        sc = s.scorecard(trades)
        # equity: 100, -50, 0, -200, 100 -> peak 100, trough -200 -> drawdown 300
        self.assertEqual(sc.max_drawdown, 300)

    def test_no_losses_profit_factor_flagged(self):
        sc = s.scorecard([{"gross": 10, "charges": 1, "net": 9}])
        self.assertTrue(math.isinf(sc.profit_factor))
        self.assertTrue(any("profit factor" in n for n in sc.notes))

    def test_empty(self):
        self.assertEqual(s.scorecard([]).trades, 0)

    def test_small_sample_warning(self):
        sc = s.scorecard([{"gross": 1, "charges": 0, "net": 1}] * 5)
        self.assertTrue(any("too few" in n for n in sc.notes))

    def test_whipsaw_count(self):
        trades = [{"net": -50, "exit_reason": "reverse_cross", "bars_held": 2},
                  {"net": -50, "exit_reason": "square_off", "bars_held": 1},
                  {"net": 50, "exit_reason": "reverse_cross", "bars_held": 1}]
        self.assertEqual(s.whipsaw_count(trades, max_bars=3), 1)


if __name__ == "__main__":
    unittest.main(verbosity=1)
