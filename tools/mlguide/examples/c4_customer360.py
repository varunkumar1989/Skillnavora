"""Customer 360 analytics file: one row per customer built from customers, products and
transactions, then heuristic and RFM segmentation on top. Synthetic data with the same shape
as the class case (an e-commerce retailer, 1 April 2012 to 31 March 2013, two half-year periods).
Run: python c4_customer360.py"""
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
START, MID, END = pd.Timestamp("2012-04-01"), pd.Timestamp("2012-10-01"), pd.Timestamp("2013-03-31")

# ---------- 1. Source tables ----------
n_cust = 600
customers = pd.DataFrame({
    "customer_id": np.arange(10001, 10001 + n_cust),
    "gender": rng.choice(["M", "F"], n_cust),
    "age": rng.integers(18, 70, n_cust),
    "join_date": END - pd.to_timedelta(rng.integers(60, 6 * 365, n_cust), unit="D"),
})
cats = ["Food", "Beauty", "Drinks", "Home", "Mobile", "Digital"]
products = pd.DataFrame({"product_id": np.arange(1, 61), "category": np.repeat(cats, 10)})
products["sale_price"] = rng.choice([49, 99, 199, 499, 1499, 9999], 60, p=[.25, .25, .2, .15, .1, .05]).astype(float)
products["cost_price"] = (products.sale_price * rng.uniform(.6, .85, 60)).round(0)
products["is_promo"] = rng.random(60) < .15

rows = []
for cid, life in zip(customers.customer_id, rng.choice(["churn", "new", "steady", "grow", "fade"], n_cust, p=[.15, .15, .4, .15, .15])):
    n_orders = rng.integers(1, 25)
    lo, hi = {"churn": (START, MID), "new": (MID, END)}.get(life, (START, END))
    dates = lo + pd.to_timedelta(rng.integers(0, (hi - lo).days, n_orders), unit="D")
    if life == "grow":   dates = dates[dates >= START + pd.Timedelta(days=120)]
    if life == "fade":   dates = dates[dates <= END - pd.Timedelta(days=120)]
    for d in dates:
        for _ in range(rng.integers(1, 4)):                           # items in the basket
            rows.append((cid, d, rng.integers(1, 61), rng.integers(1, 4), rng.uniform(0, .25)))
tx = pd.DataFrame(rows, columns=["customer_id", "order_date", "product_id", "sale_number", "disc"])
tx = tx.merge(products, on="product_id")
tx["act_amt"] = tx.sale_price * tx.sale_number
tx["sale_amount"] = (tx.act_amt * (1 - tx.disc)).round(2)            # what the customer paid
tx["cost_amt"] = tx.cost_price * tx.sale_number
tx["period"] = np.where(tx.order_date < MID, "p1", "p2")
print(f"Source tables: customers {customers.shape}, products {products.shape}, transactions {tx.shape}")

# ---------- 2. Customer 360 (one row per customer) ----------
g = tx.groupby("customer_id")
c360 = pd.DataFrame({
    "first_date": g.order_date.min(),
    "recent_date": g.order_date.max(),
    "no_baskets": g.order_date.nunique(),                             # all orders on one day = one basket
    "sale_amount": g.sale_amount.sum(),
    "act_amt": g.act_amt.sum(),
    "cost_amt": g.cost_amt.sum(),
    "quantity": g.sale_number.sum(),
    "no_prds": g.product_id.count(),
    "no_prds_promo": g.is_promo.sum(),
})
c360["margin"] = c360.sale_amount - c360.cost_amt
c360["discount"] = c360.act_amt - c360.sale_amount
c360["avg_basket_value"] = c360.sale_amount / c360.no_baskets
c360["avg_margin"] = c360.margin / c360.no_baskets
c360["margin_pct"] = c360.margin / c360.sale_amount
c360["discount_pct"] = c360.discount / c360.act_amt
c360["promo_prd_pct"] = c360.no_prds_promo / c360.no_prds
weekend = tx[tx.order_date.dt.dayofweek >= 5].groupby("customer_id").order_date.nunique()
c360["no_baskets_weekend"] = weekend.reindex(c360.index).fillna(0).astype(int)
per = tx.pivot_table(index="customer_id", columns="period", values="sale_amount", aggfunc="sum", fill_value=0)
c360["sale_amount_p1"], c360["sale_amount_p2"] = per.get("p1", 0), per.get("p2", 0)

# category counts, revenue, penetration (share of baskets with the category) and purchase flags
cat_cnt = tx.pivot_table(index="customer_id", columns="category", values="product_id", aggfunc="count", fill_value=0)
cat_amt = tx.pivot_table(index="customer_id", columns="category", values="sale_amount", aggfunc="sum", fill_value=0)
cat_bsk = tx.groupby(["customer_id", "category"]).order_date.nunique().unstack(fill_value=0)
for c in cats:
    c360[f"cat_prd_cnt_{c}"] = cat_cnt.get(c, 0)
    c360[f"cat_amt_{c}"] = cat_amt.get(c, 0).round(2)
    c360[f"cat_pen_{c}"] = (cat_bsk.get(c, 0) / c360.no_baskets).round(3)
    c360[f"cat_pur_{c}"] = (c360[f"cat_prd_cnt_{c}"] > 0).astype(int)
c360["no_distinct_categories"] = c360[[f"cat_pur_{c}" for c in cats]].sum(axis=1)
c360["multi_cat_flag"] = (c360.no_distinct_categories > 1).astype(int)
c360["buyer_flag"] = np.where(c360.no_baskets == 1, "One-time buyer", "Repeat buyer")
c360["decile_sale_amt"] = pd.qcut(c360.sale_amount.rank(method="first"), 10, labels=False)   # 0..9
c360["high_spender_flag"] = (c360.decile_sale_amt == 9).astype(int)

p1, p2 = c360.sale_amount_p1, c360.sale_amount_p2
c360["customer_segment"] = np.select(
    [(p1 == 0) & (p2 > 0), (p1 > 0) & (p2 == 0), p2 > p1, p1 > p2],
    ["New", "Churner", "Upward migrator", "Downward migrator"], default="Stable")
c360["churn_flag"] = ((p1 > 0) & (p2 == 0)).astype(int)            # target for a churn model
c360 = c360.join(customers.set_index("customer_id"))
c360["join_date"] = c360[["join_date", "first_date"]].min(axis=1)       # a customer joins on or before the first order
print(f"Customer 360 file: {c360.shape[0]} customers x {c360.shape[1]} variables")
show = ["no_baskets", "sale_amount", "avg_basket_value", "margin_pct", "cat_pen_Food", "buyer_flag", "customer_segment"]
print(c360[show].head(5).round(2).to_string())

# ---------- 3. Heuristic segmentation (rules, no model) ----------
c360["tenure_years"] = ((END - c360.join_date).dt.days / 365).round(1)
c360["loyalty_segment"] = pd.cut(c360.tenure_years, [0, 1, 3, 100], labels=["New (<1y)", "Established (1-3y)", "Loyal (3y+)"])
c360["demographic_segment"] = c360.gender + " " + pd.cut(c360.age, [17, 25, 40, 55, 100], labels=["18-25", "26-40", "41-55", "56+"]).astype(str)
c360["life_stage"] = pd.cut(c360.age, [17, 24, 34, 54, 100], labels=["Student / early job", "Young professional", "Family", "Senior"])

# ---------- 4. RFM segmentation with percentile rules ----------
c360["recency_days"] = (END - c360.recent_date).dt.days
c360["R"] = pd.qcut(c360.recency_days.rank(method="first"), 3, labels=[3, 2, 1]).astype(int)   # recent = 3
c360["F"] = pd.qcut(c360.no_baskets.rank(method="first"), 3, labels=[1, 2, 3]).astype(int)
c360["M"] = pd.qcut(c360.sale_amount.rank(method="first"), 3, labels=[1, 2, 3]).astype(int)
c360["RFM_score"] = c360.R + c360.F + c360.M
c360["RFM_tier"] = pd.cut(c360.RFM_score, [2, 5, 7, 9], labels=["Bronze", "Silver", "Gold"])

print("\nCustomer segment (period 1 vs period 2):\n" + c360.customer_segment.value_counts().to_string())
print("\nRFM tiers with average value:")
print(c360.groupby("RFM_tier", observed=True).agg(customers=("RFM_score", "size"), avg_recency_days=("recency_days", "mean"),
      avg_baskets=("no_baskets", "mean"), avg_sales=("sale_amount", "mean")).round(1).to_string())
print("\nLoyalty segments:\n" + c360.loyalty_segment.value_counts().sort_index().to_string())
print("\nLife-stage segments:\n" + c360.life_stage.value_counts().sort_index().to_string())
print(f"\nTargets ready for modelling: churn_flag rate = {c360.churn_flag.mean():.1%}, high_spender_flag rate = {c360.high_spender_flag.mean():.1%}")
