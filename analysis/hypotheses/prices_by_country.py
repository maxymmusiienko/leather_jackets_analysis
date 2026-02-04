from scipy import stats
import pandas as pd

df = pd.read_csv('C:\\Users\\Musiyenko.M\\PycharmProjects\\leather_jackets_analysis\\analysis\\regression\\cleaned_df.csv')

def compare_prices_by_country(country1, country2):
    group1 = df[df['country_code'] == country1]['log_price'].dropna()
    group2 = df[df['country_code'] == country2]['log_price'].dropna()

    n1 = len(group1)
    n2 = len(group2)

    print(f"--- Sample Size Analysis ---")
    print(f"Group 1 ({country1}): n = {n1}")
    print(f"Group 2 ({country2}): n = {n2}")
    print("-" * 30)

    stat, p_value = stats.mannwhitneyu(group1, group2, alternative='less')

    print(f"Hypothesis Test: Is {country1} cheaper than {country2}?")
    print(f"P-value: {p_value}")

    if p_value < 0.05:
        print(f"Result: Reject H0. There is significant evidence that {country1} jackets are cheaper.")
    else:
        print(f"Result: Fail to reject H0. No significant price difference found.")


compare_prices_by_country('GB', 'PK')
