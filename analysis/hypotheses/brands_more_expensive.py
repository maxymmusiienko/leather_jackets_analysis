import pandas as pd
from scipy import stats

df = pd.read_csv('C:\\Users\\Musiyenko.M\\PycharmProjects\\leather_jackets_analysis\\analysis\\regression\\cleaned_df.csv')

def compare_brand_and_common_prices():
    group1 = df[df['has_brand'] == False]['log_price']
    group2 = df[df['has_brand'] == True]['log_price']

    n1 = len(group1)
    n2 = len(group2)

    print(f"--- Sample Size Analysis ---")
    print(f"Group 1 Not branded: n = {n1}")
    print(f"Group 2 Branded: n = {n2}")
    print("-" * 30)

    stat, p_value = stats.mannwhitneyu(group1, group2, alternative='less')

    print(f"Hypothesis Test: Is not branded jackets cheaper than jackets with brands?")
    print(f"P-value: {p_value}")

    if p_value < 0.05:
        print(
            f"Result: Reject H0. There is significant evidence that not branded jackets are cheaper than branded jackets.")
    else:
        print(f"Result: Fail to reject H0. No significant price difference found.")

compare_brand_and_common_prices()
