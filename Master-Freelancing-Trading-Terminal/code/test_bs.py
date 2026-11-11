"""Tests for bs.py. Run: python3 test_bs.py"""
import math
import unittest
import bs


class BSTests(unittest.TestCase):
    def setUp(self):
        self.args = dict(S=22000.0, K=22100.0, T=5 / 365, r=0.065, sigma=0.14)

    def test_put_call_parity(self):
        c = bs.price(**self.args, kind="call")
        p = bs.price(**self.args, kind="put")
        lhs = c - p
        rhs = self.args["S"] - self.args["K"] * math.exp(-self.args["r"] * self.args["T"])
        self.assertAlmostEqual(lhs, rhs, places=6)

    def test_known_value(self):
        # Textbook check: S=K=100, T=1, r=5%, sigma=20% -> call ~10.4506
        self.assertAlmostEqual(bs.price(100, 100, 1, 0.05, 0.2, "call"), 10.4506, places=3)

    def test_delta_bounds_and_sign(self):
        self.assertTrue(0 < bs.greeks(**self.args, kind="call")["delta"] < 1)
        self.assertTrue(-1 < bs.greeks(**self.args, kind="put")["delta"] < 0)

    def test_call_put_delta_relation(self):
        dc = bs.greeks(**self.args, kind="call")["delta"]
        dp = bs.greeks(**self.args, kind="put")["delta"]
        self.assertAlmostEqual(dc - dp, math.exp(0), places=9)   # q = 0

    def test_gamma_and_vega_equal_for_call_and_put(self):
        gc = bs.greeks(**self.args, kind="call")
        gp = bs.greeks(**self.args, kind="put")
        self.assertAlmostEqual(gc["gamma"], gp["gamma"], places=12)
        self.assertAlmostEqual(gc["vega"], gp["vega"], places=12)

    def test_theta_negative_for_long_atm_option(self):
        self.assertLess(bs.greeks(**self.args, kind="call")["theta"], 0)

    def test_implied_vol_round_trip(self):
        for kind in ("call", "put"):
            mkt = bs.price(**self.args, kind=kind)
            iv = bs.implied_vol(mkt, self.args["S"], self.args["K"], self.args["T"], self.args["r"], kind)
            self.assertAlmostEqual(iv, self.args["sigma"], places=5)

    def test_rejects_bad_inputs(self):
        with self.assertRaises(ValueError):
            bs.price(0, 100, 1, 0.05, 0.2)
        with self.assertRaises(ValueError):
            bs.implied_vol(1e6, 100, 100, 1, 0.05, "call")   # above the upper bound


if __name__ == "__main__":
    unittest.main(verbosity=1)
