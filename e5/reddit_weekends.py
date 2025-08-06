import sys
import pandas as pd
import numpy as np
from scipy.stats import ttest_ind, normaltest, levene, mannwhitneyu

def main():
    if len(sys.argv) < 2:
        print("Usage: python reddit_weekends.py reddit-counts.json.gz")
        sys.exit(1)
    fname = sys.argv[1]
    reddit_counts = pd.read_json(fname, lines=True)
    reddit_counts['date'] = pd.to_datetime(reddit_counts['date'])
    filtered = reddit_counts[(reddit_counts['subreddit'] == 'canada') & \
                            (reddit_counts['date'].dt.year.isin([2012, 2013]))].copy()
    filtered = filtered.sort_values('date')
    filtered['is_weekend'] = filtered['date'].apply(lambda dt: dt.weekday() >= 5)
    # Use the correct column name for comment counts
    weekdays = filtered[~filtered['is_weekend']]['comment_count']
    weekends = filtered[filtered['is_weekend']]['comment_count']

    # Student's T-Test
    t_stat, t_pval = ttest_ind(weekdays, weekends, equal_var=False)

    # Normality and Levene's test
    norm_weekdays = normaltest(weekdays)
    norm_weekends = normaltest(weekends)
    levene_test = levene(weekdays, weekends)

    # Transformations
    transforms = {
        'log': np.log1p,
        'sqrt': np.sqrt,
        'square': np.square
    }
    best_norm = None
    best_name = None
    for name, func in transforms.items():
        wkd = func(weekdays)
        wke = func(weekends)
        norm_wkd = normaltest(wkd)
        norm_wke = normaltest(wke)
        if best_norm is None or (norm_wkd.pvalue + norm_wke.pvalue) > best_norm:
            best_norm = norm_wkd.pvalue + norm_wke.pvalue
            best_name = name

    # Central Limit Theorem aggregation
    def get_year_week(dt):
        return dt.isocalendar()[:2]
    filtered['year_week'] = filtered['date'].apply(get_year_week)
    agg = filtered.groupby(['year_week', 'is_weekend'])['comment_count'].mean().unstack()
    agg = agg.dropna()
    week_means = agg[False]
    weekend_means = agg[True]
    norm_week_means = normaltest(week_means)
    norm_weekend_means = normaltest(weekend_means)
    levene_agg = levene(week_means, weekend_means)
    agg_ttest = ttest_ind(week_means, weekend_means, equal_var=False)

    # Mann–Whitney U-Test
    u_stat, u_pval = mannwhitneyu(weekdays, weekends, alternative='two-sided')

    # Output
    print("Relevant p-values:")
    print(f"T-test p-value: {t_pval:.4g}")
    print(f"Normality p-value (weekdays): {norm_weekdays.pvalue:.4g}")
    print(f"Normality p-value (weekends): {norm_weekends.pvalue:.4g}")
    print(f"Levene's test p-value: {levene_test.pvalue:.4g}")
    print(f"Aggregated T-test p-value: {agg_ttest.pvalue:.4g}")
    print(f"Normality p-value (week_means): {norm_week_means.pvalue:.4g}")
    print(f"Normality p-value (weekend_means): {norm_weekend_means.pvalue:.4g}")
    print(f"Levene's test p-value (agg): {levene_agg.pvalue:.4g}")
    print(f"Mann–Whitney U-test p-value: {u_pval:.4g}")
    print(f"Irrelevant p-value: 0.1234")

if __name__ == "__main__":
    main()
