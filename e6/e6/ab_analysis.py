import sys
import pandas as pd
from scipy.stats import fisher_exact, mannwhitneyu

OUTPUT_TEMPLATE = (
    '"Did more/less users use the search feature?" p-value:  {more_users_p:.3g}\n'
    '"Did users search more/less?" p-value:  {more_searches_p:.3g} \n'
    '"Did more/less instructors use the search feature?" p-value:  {more_instr_p:.3g}\n'
    '"Did instructors search more/less?" p-value:  {more_instr_searches_p:.3g}'
)


def run_ab_test(df):
    # treatment: odd uid, control: even uid
    treated = df[df['uid'] % 2 == 1]
    control = df[df['uid'] % 2 == 0]

    # test 1: fraction of users with at least one search
    treated_search = (treated['search_count'] > 0).sum()
    treated_nosearch = (treated['search_count'] == 0).sum()
    control_search = (control['search_count'] > 0).sum()
    control_nosearch = (control['search_count'] == 0).sum()
    contingency = [[treated_search, treated_nosearch], [control_search, control_nosearch]]
    _, p1 = fisher_exact(contingency)

    # test 2: number of searches per user (nonparametric)
    _, p2 = mannwhitneyu(treated['search_count'], control['search_count'], alternative='two-sided')
    return p1, p2


def main():
    if len(sys.argv) < 2:
        print("Usage: python ab_analysis.py <searches.json>")
        sys.exit(1)

    df = pd.read_json(sys.argv[1], orient='records', lines=True)
    # overall
    p1, p2 = run_ab_test(df)
    # instructors only
    df_instr = df[df['is_instructor']]
    p3, p4 = run_ab_test(df_instr)

    print(OUTPUT_TEMPLATE.format(
        more_users_p=p1,
        more_searches_p=p2,
        more_instr_p=p3,
        more_instr_searches_p=p4,
    ))


if __name__ == '__main__':
    main()
