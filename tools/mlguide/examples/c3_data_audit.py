"""Analytics project lifecycle, step 2: the data audit, then step 5: the KPI views a dashboard needs.
A reusable audit function you can point at any table. Run: python c3_data_audit.py"""
import numpy as np
import pandas as pd

rng = np.random.default_rng(5)
n = 1200
sales = pd.DataFrame({
    "order_id": np.arange(1, n + 1),
    "order_date": pd.to_datetime("2026-04-01") + pd.to_timedelta(rng.integers(0, 183, n), unit="D"),
    "rep": rng.choice(["Asha", "Ravi", "Meera", "John", "Sana"], n),
    "region": rng.choice(["North", "South", "East", "West", None], n, p=[.27, .27, .2, .2, .06]),
    "product": rng.choice(["Soap", "Shampoo", "Detergent", "Toothpaste"], n),
    "qty": rng.integers(1, 40, n),
    "unit_price": rng.choice([35.0, 120.0, 210.0, 55.0], n),
})
sales["amount"] = sales.qty * sales.unit_price
sales.loc[rng.choice(n, 8, replace=False), "amount"] = 250000.0        # data-entry outliers
sales = pd.concat([sales, sales.sample(15, random_state=1)])            # duplicate rows


def data_audit(df: pd.DataFrame) -> pd.DataFrame:
    """One row per column: type, missing share, distinct values and the range that shows outliers."""
    out = []
    for c in df.columns:
        s = df[c]
        row = {"column": c, "dtype": str(s.dtype), "missing_%": round(s.isna().mean() * 100, 1), "distinct": s.nunique()}
        if pd.api.types.is_numeric_dtype(s):
            row.update(min=s.min(), p1=s.quantile(.01), median=s.median(), p99=s.quantile(.99), max=s.max())
        out.append(row)
    return pd.DataFrame(out).set_index("column")


pd.set_option("display.width", 140)
print("STEP 2  Data audit")
print(f"rows={len(sales)}  duplicate rows={sales.duplicated().sum()}")
print(data_audit(sales).round(1).to_string())

print("\nSTEP 3  Cleaning decisions taken from the audit")
clean = sales.drop_duplicates().copy()
clean["region"] = clean["region"].fillna("Unknown")
cap = clean["amount"].quantile(.99)
print(f"- removed {len(sales) - len(clean)} duplicates; filled {int(sales.region.isna().sum())} missing regions with 'Unknown'")
print(f"- capped amount at the 99th percentile ({cap:,.0f}); {(clean.amount > cap).sum()} rows changed")
clean["amount"] = clean["amount"].clip(upper=cap)

print("\nSTEP 5  KPI views for the dashboard")
target = pd.Series({"Asha": 550000, "Ravi": 500000, "Meera": 450000, "John": 480000, "Sana": 470000})
kpi = clean.groupby("rep").agg(revenue=("amount", "sum"), orders=("order_id", "count"))
kpi["target"] = target
kpi["achieved_%"] = (kpi.revenue / kpi.target * 100).round(1)
kpi["status"] = np.where(kpi["achieved_%"] >= 100, "On target", "Behind")
print(kpi.sort_values("achieved_%", ascending=False).to_string(float_format=lambda v: f"{v:,.0f}"))
monthly = clean.groupby(clean.order_date.dt.to_period("M")).amount.sum()
print("\nMonthly revenue trend:\n" + monthly.to_string(float_format=lambda v: f"{v:,.0f}"))
