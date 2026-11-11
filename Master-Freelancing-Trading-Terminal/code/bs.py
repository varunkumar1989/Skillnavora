"""Black-Scholes pricing, Greeks and implied volatility, standard library only.

European options (NSE index options such as Nifty 50 are European-style).
Inputs: S spot, K strike, T time to expiry in years, r risk-free rate (decimal), q dividend yield,
sigma volatility (decimal). Theta is per calendar day; vega and rho per 1% move (divide by 100 to
get per 1 vol point). Check the convention you need before comparing with a vendor.
"""
import math

SQRT2PI = math.sqrt(2 * math.pi)


def _pdf(x):
    return math.exp(-0.5 * x * x) / SQRT2PI


def _cdf(x):
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def _d1d2(S, K, T, r, q, sigma):
    if S <= 0 or K <= 0 or sigma <= 0 or T <= 0:
        raise ValueError("S, K, sigma and T must be positive")
    d1 = (math.log(S / K) + (r - q + 0.5 * sigma * sigma) * T) / (sigma * math.sqrt(T))
    return d1, d1 - sigma * math.sqrt(T)


def price(S, K, T, r, sigma, kind="call", q=0.0):
    """Theoretical price of a European call or put."""
    d1, d2 = _d1d2(S, K, T, r, q, sigma)
    df_r, df_q = math.exp(-r * T), math.exp(-q * T)
    if kind == "call":
        return S * df_q * _cdf(d1) - K * df_r * _cdf(d2)
    if kind == "put":
        return K * df_r * _cdf(-d2) - S * df_q * _cdf(-d1)
    raise ValueError("kind must be 'call' or 'put'")


def greeks(S, K, T, r, sigma, kind="call", q=0.0):
    """Delta, gamma, theta (per day), vega (per 1 vol point), rho (per 1% rate)."""
    d1, d2 = _d1d2(S, K, T, r, q, sigma)
    df_r, df_q = math.exp(-r * T), math.exp(-q * T)
    gamma = df_q * _pdf(d1) / (S * sigma * math.sqrt(T))
    vega = S * df_q * _pdf(d1) * math.sqrt(T) / 100.0
    if kind == "call":
        delta = df_q * _cdf(d1)
        theta = (-S * df_q * _pdf(d1) * sigma / (2 * math.sqrt(T))
                 - r * K * df_r * _cdf(d2) + q * S * df_q * _cdf(d1)) / 365.0
        rho = K * T * df_r * _cdf(d2) / 100.0
    elif kind == "put":
        delta = -df_q * _cdf(-d1)
        theta = (-S * df_q * _pdf(d1) * sigma / (2 * math.sqrt(T))
                 + r * K * df_r * _cdf(-d2) - q * S * df_q * _cdf(-d1)) / 365.0
        rho = -K * T * df_r * _cdf(-d2) / 100.0
    else:
        raise ValueError("kind must be 'call' or 'put'")
    return {"delta": delta, "gamma": gamma, "theta": theta, "vega": vega, "rho": rho}


def implied_vol(market_price, S, K, T, r, kind="call", q=0.0, lo=1e-4, hi=5.0, tol=1e-8, max_iter=200):
    """Implied volatility by bisection. Raises ValueError if the price is outside no-arbitrage bounds."""
    df_r, df_q = math.exp(-r * T), math.exp(-q * T)
    intrinsic = max(0.0, (S * df_q - K * df_r) if kind == "call" else (K * df_r - S * df_q))
    if market_price < intrinsic - 1e-9 or market_price >= (S * df_q if kind == "call" else K * df_r):
        raise ValueError("market price violates no-arbitrage bounds")
    f = lambda v: price(S, K, T, r, v, kind, q) - market_price
    a, b = lo, hi
    if f(a) * f(b) > 0:
        raise ValueError("no implied volatility found in the search range")
    for _ in range(max_iter):
        m = 0.5 * (a + b)
        fm = f(m)
        if abs(fm) < tol or (b - a) < tol:
            return m
        if f(a) * fm <= 0:
            b = m
        else:
            a = m
    return 0.5 * (a + b)
