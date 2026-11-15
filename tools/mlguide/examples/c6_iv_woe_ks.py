"""Credit-risk toolkit used in Indian banking and analytics interviews:
WOE and Information Value to screen variables, then a decile gains table with lift, KS and Gini
to judge a loan-default model. Synthetic bank-loans data shaped like the class case.
Run: python c6_iv_woe_ks.py"""
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

rng = np.random.default_rng(8)
n = 3000
df = pd.DataFrame({
    "age": rng.integers(21, 60, n),
    "employ_years": rng.integers(0, 25, n),
    "address_years": rng.integers(0, 20, n),
    "income_k": rng.lognormal(3.6, .5, n).round(1),
    "debt_income_pct": rng.gamma(2.2, 4.5, n).round(1),
    "credit_card_debt_k": rng.gamma(1.4, 1.2, n).round(2),
    "education": rng.choice(["School", "Graduate", "Postgraduate"], n, p=[.45, .4, .15]),
    "phone_brand": rng.choice(["A", "B", "C"], n),                                  # should be useless
})
logit = (-1.4 + .11 * df.debt_income_pct + .25 * df.credit_card_debt_k - .09 * df.employ_years
         - .03 * df.address_years - .01 * (df.age - 35) + np.where(df.education == "School", .25, 0))
df["default"] = (rng.random(n) < 1 / (1 + np.exp(-logit))).astype(int)
print(f"{n} loans, default rate {df.default.mean():.1%}\n")


def woe_iv(x, y, bins=5):
    """Bin x (quantiles for numbers, categories as they are), then WOE = ln(%good / %bad) per bin
    and IV = sum((%good - %bad) * WOE). A small constant avoids log(0)."""
    groups = pd.qcut(x, bins, duplicates="drop") if pd.api.types.is_numeric_dtype(x) else x
    t = pd.crosstab(groups, y)
    good, bad = (t[0] + .5) / (t[0].sum() + .5), (t[1] + .5) / (t[1].sum() + .5)
    woe = np.log(good / bad)
    return float(((good - bad) * woe).sum()), pd.DataFrame({"loans": t.sum(axis=1), "default_rate": (t[1] / t.sum(axis=1)).round(3), "WOE": woe.round(3)})


def strength(iv):
    return "useless" if iv < .02 else "weak" if iv < .1 else "medium" if iv < .3 else "strong" if iv < .5 else "suspicious (check for leakage)"


ivs = {c: woe_iv(df[c], df.default)[0] for c in df.columns if c != "default"}
print("Information Value (screen variables before modelling)")
for c, iv in sorted(ivs.items(), key=lambda kv: -kv[1]):
    print(f"  {c:<20} IV = {iv:.3f}  {strength(iv)}")
print("\nWOE table for debt_income_pct (WOE falls as risk rises: a monotonic pattern is what you want):")
print(woe_iv(df.debt_income_pct, df.default)[1].to_string())

keep = [c for c, iv in ivs.items() if iv >= .02]                              # drop "useless" variables
cats = [c for c in keep if not pd.api.types.is_numeric_dtype(df[c])]
X = pd.get_dummies(df[keep], columns=cats, drop_first=True, dtype=float)
X_tr, X_te, y_tr, y_te = train_test_split(X, df.default, test_size=.3, random_state=8, stratify=df.default)
sc = StandardScaler().fit(X_tr)
model = LogisticRegression(max_iter=1000).fit(sc.transform(X_tr), y_tr)
p = model.predict_proba(sc.transform(X_te))[:, 1]
print(f"\nLogistic regression on the {len(keep)} variables with IV >= 0.02: {keep}")

# Gains table: sort by predicted risk, cut into 10 deciles, count defaulters in each
g = pd.DataFrame({"p": p, "y": y_te.values}).sort_values("p", ascending=False)
g["decile"] = np.arange(len(g)) * 10 // len(g) + 1
tab = g.groupby("decile").agg(loans=("y", "size"), defaults=("y", "sum"))
tab["non_defaults"] = tab.loans - tab.defaults
tab["default_rate"] = (tab.defaults / tab.loans).round(3)
tab["cum_%_defaults"] = (tab.defaults.cumsum() / tab.defaults.sum() * 100).round(1)
tab["cum_%_good"] = (tab.non_defaults.cumsum() / tab.non_defaults.sum() * 100).round(1)
tab["KS"] = (tab["cum_%_defaults"] - tab["cum_%_good"]).round(1)
tab["lift"] = (tab.default_rate / g.y.mean()).round(2)
print("\nGains table on the test set (decile 1 = riskiest 10%)")
print(tab.to_string())
auc = roc_auc_score(y_te, p)
print(f"\nKS = {tab.KS.max():.1f} at decile {tab.KS.idxmax()} | AUC = {auc:.3f} | Gini = 2*AUC - 1 = {2 * auc - 1:.3f}")
print(f"Reading: rejecting the riskiest 30% of applicants catches {tab['cum_%_defaults'].iloc[2]:.0f}% of the defaulters.")
