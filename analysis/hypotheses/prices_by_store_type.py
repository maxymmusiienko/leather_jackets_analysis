import pandas as pd
from scipy import stats

df = pd.read_csv('C:\\Users\\Musiyenko.M\\PycharmProjects\\leather_jackets_analysis\\analysis\\regression\\cleaned_df.csv')

"""
H0 - Prices on leather jackets in local stores are equal to International stores
"""

def compare_prices_by_store_type():
    group1 = df[df['store_type'] == 'Local']['log_price']
    group2 = df[df['store_type'] == 'International']['log_price']

    n1 = len(group1)
    n2 = len(group2)

    print(f"--- Sample Size Analysis ---")
    print(f"Group 1 Local: n = {n1}")
    print(f"Group 2 International: n = {n2}")
    print("-" * 30)

    stat, p_value = stats.mannwhitneyu(group1, group2, alternative='less')

    print(f"Hypothesis Test: Is Local stores cheaper than International stores?")
    print(f"P-value: {p_value}")

    if p_value < 0.05:
        print(f"Result: Reject H0. There is significant evidence that Local store jackets are cheaper than International stores.")
    else:
        print(f"Result: Fail to reject H0. No significant price difference found.")

compare_prices_by_store_type()
