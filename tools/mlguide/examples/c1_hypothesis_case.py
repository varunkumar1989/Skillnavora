"""Hypothesis-testing case study: does a credit-card campaign change usage?
Synthetic data with the same structure as the class case (customer segments, regions,
usage before and after a campaign). Run: python c1_hypothesis_case.py"""
import numpy as np
import pandas as pd
from scipy import stats

rng = np.random.default_rng(7)
n = 200
df = pd.DataFrame({
    "cust_id": range(1, n + 1),
    "sex": rng.integers(0, 2, n),                 # 0 = male, 1 = female
    "region": rng.choice([1, 2, 3, 4], n),        # 1 North, 2 South, 3 East, 4 West
})
df["segment"] = np.where(df.region <= 2, rng.choice([1, 2, 3], n, p=[.5, .3, .2]), rng.choice([1, 2, 3], n, p=[.2, .3, .5]))
df["pre_usage"] = rng.normal(50, 12, n).round(1)
df["post_usage_1month"] = (df.pre_usage + rng.normal(0.6, 8, n)).round(1)      # tiny change
df["post_usage_2ndmonth"] = (df.pre_usage + rng.normal(4.0, 8, n)).round(1)   # real lift
df["latest_mon_usage"] = (df.post_usage_2ndmonth + df.segment * 3 + rng.normal(0, 6, n)).round(1)

print("Data audit:", df.shape, "| missing:", int(df.isnull().sum().sum()), "| duplicates:", int(df.duplicated().sum()))
ALPHA = 0.05  # 95% confidence
rows = []


def decide(name, h0, p, test):
    verdict = "Reject H0" if p < ALPHA else "Fail to reject H0"
    rows.append((name, test, h0, f"{p:.4f}", verdict))


# Q1 One-sample t-test: is the average post-campaign usage different from the old average of 50?
t, p = stats.ttest_1samp(df.post_usage_1month, popmean=50)
decide("Q1 sample vs population", "mean usage = 50", p, "one-sample t")

# Q2 Paired (dependent) t-test, one-tailed: did usage go UP in month 1?
t, p = stats.ttest_rel(df.post_usage_1month, df.pre_usage, alternative="greater")
decide("Q2 before vs after (month 1)", "post <= pre", p, "paired t, one-tailed")

# Q2b same question for month 2
t, p = stats.ttest_rel(df.post_usage_2ndmonth, df.pre_usage, alternative="greater")
decide("Q2b before vs after (month 2)", "post <= pre", p, "paired t, one-tailed")

# Q3 Independent two-sample t-test (Welch): do men and women use the card differently?
m, f = df.loc[df.sex == 0, "latest_mon_usage"], df.loc[df.sex == 1, "latest_mon_usage"]
t, p = stats.ttest_ind(m, f, equal_var=False)
decide("Q3 male vs female", "mean_m = mean_f", p, "independent t (Welch)")

# Q4 One-way ANOVA: is usage the same in all three segments?
groups = [g.latest_mon_usage for _, g in df.groupby("segment")]
F, p = stats.f_oneway(*groups)
decide("Q4 three segments", "all segment means equal", p, "one-way ANOVA")

# Q5 Chi-square test of independence: are segment and region related?
obs = pd.crosstab(df.region, df.segment)
chi2, p, dof, expected = stats.chi2_contingency(obs)
decide("Q5 segment vs region", "independent", p, f"chi-square (df={dof})")

# Q6 Correlation: does pre-campaign usage move with latest usage?
r, p = stats.pearsonr(df.pre_usage, df.latest_mon_usage)
decide(f"Q6 Pearson r = {r:.2f}", "no linear correlation", p, "Pearson")
rho, p = stats.spearmanr(df.pre_usage, df.latest_mon_usage)
decide(f"Q6b Spearman rho = {rho:.2f}", "no monotonic correlation", p, "Spearman")

print(f"\n{'Question':<30}{'Test':<24}{'H0':<26}{'p-value':<10}Decision (alpha 0.05)")
for r_ in rows:
    print(f"{r_[0]:<30}{r_[1]:<24}{r_[2]:<26}{r_[3]:<10}{r_[4]}")

# Assumption check and the non-parametric versions
w, p_norm = stats.shapiro(df.post_usage_1month - df.pre_usage)
print(f"\nShapiro-Wilk on paired differences: p = {p_norm:.3f} ({'looks normal' if p_norm > ALPHA else 'not normal: use Wilcoxon'})")
print(f"Wilcoxon signed-rank (month 2 > pre): p = {stats.wilcoxon(df.post_usage_2ndmonth, df.pre_usage, alternative='greater').pvalue:.2e}")
print(f"Mann-Whitney U (male vs female):      p = {stats.mannwhitneyu(m, f).pvalue:.4f}")
print(f"Kruskal-Wallis (three segments):      p = {stats.kruskal(*groups).pvalue:.2e}")
print("\nObserved counts (region x segment):\n" + obs.to_string())
print(f"\nCritical values: z (two-tailed, 95 pct) = {stats.norm.ppf(0.975):.2f} | t (df=199, two-tailed) = {stats.t.ppf(0.975, 199):.2f} | chi-square (df={dof}) = {stats.chi2.ppf(0.95, dof):.2f}")
