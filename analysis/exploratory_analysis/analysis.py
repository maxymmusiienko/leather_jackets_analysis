import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import normaltest

FILE_NAME = 'C:\\Users\\Musiyenko.M\\PycharmProjects\\leather_jackets_analysis\\analysis\\masters_jackets_data.csv'
df = pd.read_csv(FILE_NAME)

def plot_price_histogram():
    bins = [0, 10, 25, 50, 75, 100, 150, 200, 300, 500, 10000]
    df['price_category'] = pd.cut(df['price($)'], bins=bins)
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(10,10))
    sns.countplot(data=df, x='price_category', palette='viridis')

    plt.title('Histogram of leather jackets prices', fontsize=20)
    plt.xlabel('Price($)', fontsize=14)
    plt.ylabel('Amount of announcements', fontsize=14)

    plt.show()

def boxplot_price():
    sns.boxplot(x = df['price($)'])
    plt.title('Boxplot of leather jackets prices', fontsize=20)
    plt.show()

def get_basic_price_stats():
    price_stats = df['price($)'].describe()
    minimum, maximum = price_stats['min'], price_stats['max']
    mean = price_stats['mean']
    median = price_stats['50%']
    q1 = price_stats['25%']
    q3 = price_stats['75%']

    price_range = maximum - minimum
    mode = df['price($)'].mode()[0]

    variance = df['price($)'].var()

    std_dev = df['price($)'].std()

    print(f"--- Descriptive Statistics ---")
    print(f"Min: {minimum:.2f} | Max: {maximum:.2f}")
    print(f"Mean (Expected Value): {mean:.2f}")
    print(f"Median: {median:.2f}")
    print(f"Mode: {mode:.2f}")
    print(f"Q1 (25th percentile): {q1:.2f}")
    print(f"Q3 (75th percentile): {q3:.2f}")
    print(f"Range: {price_range:.2f}")
    print(f"Variance: {variance:.2f}")
    print(f"Standard Deviation: {std_dev:.2f}")

def normal_dist_price_test_k2():
    "H0 - price($) is normal distributed"
    stat, p = normaltest(df['price($)'])

    print('H0: price($) is normal distributed')
    print(f'Statistics={stat:.3f}, p-value={p}')

    if p > 0.05:
        print('Result: Sample looks Gaussian (fail to reject H0)')
    else:
        print('Result: Sample does not look Gaussian (reject H0)')

normal_dist_price_test_k2()
