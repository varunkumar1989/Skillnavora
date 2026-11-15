"""End-to-end linear regression case study: what drives car sales?
Every preprocessing step from the classes in one script: data audit, train/test split,
outlier capping, missing-value imputation (SimpleImputer vs KNNImputer), encoding, VIF
feature selection, statsmodels OLS, evaluation and an over/underfitting check.
Rule used throughout: learn every preprocessing value (percentiles, medians, neighbours)
from the TRAINING set only, then apply it to the test set, so the test stays unseen.
Synthetic data shaped like the class's car-sales file. Run: python c5_car_sales_regression.py"""
import numpy as np
import pandas as pd
import statsmodels.api as sm
from sklearn.impute import KNNImputer, SimpleImputer
from sklearn.metrics import mean_absolute_percentage_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from statsmodels.stats.outliers_influence import variance_inflation_factor

rng = np.random.default_rng(21)
n = 200
brands = ["Maruti", "Hyundai", "Tata", "Honda", "Toyota", "Kia", "Mahindra", "Skoda"]
df = pd.DataFrame({
    "brand": rng.choice(brands, n),
    "vehicle_type": rng.choice(["Hatchback", "Sedan", "SUV"], n, p=[.4, .3, .3]),
    "engine_size": rng.normal(1.6, .45, n).clip(.8, 3.5).round(1),
})
df["horsepower"] = (55 * df.engine_size + rng.normal(10, 9, n)).round(0)
df["curb_weight"] = (750 + 280 * df.engine_size + np.where(df.vehicle_type == "SUV", 250, 0) + rng.normal(0, 60, n)).round(0)
df["length_mm"] = (3700 + 0.9 * (df.curb_weight - 750) + rng.normal(0, 90, n)).round(0)
df["fuel_capacity"] = (35 + 0.012 * df.curb_weight + rng.normal(0, 3, n)).round(1)
df["fuel_efficiency"] = (27 - 3.2 * df.engine_size + rng.normal(0, 1.4, n)).round(1)
df["price_lakh"] = (2.5 + 4.2 * df.engine_size + np.where(df.vehicle_type == "SUV", 3, 0) + rng.normal(0, 1.2, n)).round(2)
df["resale_value_lakh"] = (df.price_lakh * rng.uniform(.45, .85, n) + rng.normal(0, .8, n)).round(2)
log_sales = 4.2 - 0.12 * df.price_lakh + 0.06 * df.fuel_efficiency + np.where(df.vehicle_type == "SUV", .25, 0) + rng.normal(0, .18, n)
df["sales_thousands"] = np.exp(log_sales).round(2)
for col, k in [("resale_value_lakh", 35), ("fuel_efficiency", 8), ("curb_weight", 5)]:
    df.loc[rng.choice(n, k, replace=False), col] = np.nan                        # missing values
bad = rng.choice(n, 4, replace=False)
df.loc[bad, "horsepower"] *= 10                                                  # data-entry errors (extra zero)
df.loc[bad[:2], "price_lakh"] *= 10

# STEP 1 Data audit
print("STEP 1  Data audit")
num = [c for c in df.select_dtypes("number").columns if c != "sales_thousands"]
audit = pd.DataFrame({"missing": df[num].isna().sum(), "p1": df[num].quantile(.01), "median": df[num].median(),
                      "p99": df[num].quantile(.99), "max": df[num].max()}).round(2)
print(audit.to_string())

# STEP 2 Split BEFORE any treatment that learns from the data
train, test = train_test_split(df, test_size=0.3, random_state=1)
train, test = train.copy(), test.copy()
print(f"\nSTEP 2  Train/test split 70:30 -> train {len(train)} cars, test {len(test)} cars")

# STEP 3 Outlier capping with limits learned on train
hp = train.horsepower
q1, q3 = hp.quantile([.25, .75])
print(f"\nSTEP 3  Three outlier rules for horsepower (train): IQR fences [{q1 - 1.5 * (q3 - q1):.0f}, {q3 + 1.5 * (q3 - q1):.0f}] | "
      f"mean +/- 3 SD [{hp.mean() - 3 * hp.std():.0f}, {hp.mean() + 3 * hp.std():.0f}] | percentiles [{hp.quantile(.01):.0f}, {hp.quantile(.99):.0f}]")
print("        the 99th percentile still sits inside the errors (more than 1% of rows are wrong), so cap with the IQR fences")


def iqr_fences(s):
    a, b = s.quantile([.25, .75])
    return a - 1.5 * (b - a), b + 1.5 * (b - a)


limits = {c: iqr_fences(train[c]) for c in num}
before = int((train.horsepower > limits["horsepower"][1]).sum())
for part in (train, test):
    for c, (lo, hi) in limits.items():
        part[c] = part[c].clip(lo, hi)
print(f"        capped every numeric column at its train IQR fences: {before} horsepower values capped, max {df.horsepower.max():.0f} -> {train.horsepower.max():.0f}")

# STEP 4 Missing values: compare SimpleImputer (median) and KNNImputer, both fitted on train
mask = test.resale_value_lakh.isna()
expected = test.price_lakh[mask] * .65                                           # what resale should be on average
simple = SimpleImputer(strategy="median").fit(train[num])
knn = KNNImputer(n_neighbors=5).fit(train[num])
err_s = np.abs(pd.DataFrame(simple.transform(test[num]), columns=num, index=test.index).resale_value_lakh[mask] - expected).mean()
err_k = np.abs(pd.DataFrame(knn.transform(test[num]), columns=num, index=test.index).resale_value_lakh[mask] - expected).mean()
print(f"\nSTEP 4  {int(mask.sum())} missing resale values in test: average error SimpleImputer(median) {err_s:.2f} lakh | KNNImputer(k=5) {err_k:.2f} lakh -> using KNNImputer")
train[num] = knn.transform(train[num])
test[num] = knn.transform(test[num])

# STEP 5 Encoding: one-hot with drop_first (avoids the dummy-variable trap); log of the skewed target
train = pd.get_dummies(train, columns=["vehicle_type", "brand"], drop_first=True, dtype=float)
test = pd.get_dummies(test, columns=["vehicle_type", "brand"], drop_first=True, dtype=float).reindex(columns=train.columns, fill_value=0)
for part in (train, test):
    part["ln_sales"] = np.log(part.sales_thousands)
print(f"\nSTEP 5  One-hot encoding -> {train.shape[1] - 2} features; target ln(sales): skew {train.sales_thousands.skew():.2f} -> {train.ln_sales.skew():.2f}")

# STEP 6 VIF: drop the worst variable until every VIF <= 5, but keep what the business must explain
features = [c for c in train.columns if c not in ("sales_thousands", "ln_sales")]
KEEP = {"price_lakh"}                                                            # the lever the client controls
print("\nSTEP 6  VIF elimination (multicollinearity), protecting", sorted(KEEP))
while True:
    X = sm.add_constant(train[features])
    vif = pd.Series([variance_inflation_factor(X.values, i) for i in range(1, X.shape[1])], index=features)
    worst = vif.drop(list(KEEP)).idxmax()
    if vif[worst] <= 5:
        break
    print(f"        drop {worst:<18} VIF = {vif[worst]:5.1f}")
    features.remove(worst)
print(f"        kept {len(features)} features, max VIF {vif.max():.2f}")


def fit_and_score(feats, label):
    model = sm.OLS(train.ln_sales, sm.add_constant(train[feats])).fit()
    res = {}
    for name, part in (("train", train), ("test", test)):
        pred = np.exp(model.predict(sm.add_constant(part[feats], has_constant="add")))
        res[name] = (np.sqrt(mean_squared_error(part.sales_thousands, pred)), mean_absolute_percentage_error(part.sales_thousands, pred),
                     r2_score(part.sales_thousands, pred))
    print(f"\n{label}: {len(feats)} features, adjusted R2 on train {model.rsquared_adj:.3f}")
    print(f"        {'':6}{'RMSE':>8}{'MAPE':>8}{'R2':>8}")
    for name in ("train", "test"):
        print(f"        {name:<6}{res[name][0]:8.2f}{res[name][1]:8.1%}{res[name][2]:8.3f}")
    ratio = res["test"][0] / res["train"][0]
    print("        verdict:", "overfitting (test error much higher than train)" if ratio > 1.3
          else "underfitting (both errors high)" if res["train"][2] < .3 else "good fit: train and test errors are close")
    return model


# STEP 7 Full model, then STEP 8 keep only significant drivers (p < 0.05) and refit
model = fit_and_score(features, "STEP 7  OLS with all VIF-screened features")
sig = model.pvalues.drop("const")
drivers = list(sig[sig < .05].index)
model = fit_and_score(drivers, "STEP 8  OLS with significant drivers only")
print("\n        driver               coef    effect on sales per unit")
for f in drivers:
    print(f"        {f:<20}{model.params[f]:+.3f}   about {np.expm1(model.params[f]) * 100:+.1f}%")
print(f"        equation: ln(sales) = {model.params['const']:.2f} " + " ".join(f"{v:+.3f}*{k}" for k, v in model.params.drop('const').items()))
