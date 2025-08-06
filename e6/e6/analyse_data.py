import pandas as pd
from scipy.stats import f_oneway, ttest_ind
import itertools

# Read data
df = pd.read_csv('data.csv')

# Group by implementation
grouped = {name: group['time'].values for name, group in df.groupby('implementation')}
implementations = list(grouped.keys())

# ANOVA test
f_stat, p_anova = f_oneway(*grouped.values())
print(f"ANOVA test across implementations: F={f_stat:.3g}, p-value={p_anova:.3g}")

# Mean times
means = df.groupby('implementation')['time'].mean().sort_values()
print("\nMean execution times (seconds):")
for name, m in means.items():
    print(f"{name}: {m:.6f}")

# Pairwise t-tests with Bonferroni correction
impl_list = means.index.tolist()
pairs = list(itertools.combinations(impl_list, 2))
alpha = 0.05
print(f"\nPairwise t-tests (Bonferroni corrected alpha={alpha/len(pairs):.5f}):")
for i, j in pairs:
    g1 = grouped[i]
    g2 = grouped[j]
    p = ttest_ind(g1, g2, equal_var=False).pvalue
    p_corr = p * len(pairs)
    significant = p_corr < alpha
    status = "significant" if significant else "not significant"
    print(f"{i} vs {j}: p={p:.3g}, p_corr={p_corr:.3g} -> {status}")
