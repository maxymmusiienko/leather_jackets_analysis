import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import patches
from scipy import stats
import numpy as np

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

def normal_dist_test_k2(data_frame, param):
    "H0 - param is normal distributed"
    stat, p = stats.normaltest(data_frame[param])

    print(f'H0: {param} is normal distributed')
    print(f'Statistics={stat:.3f}, p-value={p}')

    if p > 0.05:
        print('Result: Sample looks Gaussian (fail to reject H0)')
    else:
        print('Result: Sample does not look Gaussian (reject H0)')

def qq_plot(data_frame, param):
    plt.figure(figsize=(8, 6))
    stats.probplot(data_frame[param], dist="norm", plot=plt)
    plt.title(f"Q-Q Plot: {param} Distribution")
    plt.show()

def avg_announcement_length_by_store():
    sns.set_style("whitegrid")
    plt.figure(figsize=(10, 6))

    sns.barplot(data=df, x='store_name', y='title_length', palette='viridis', capsize=.1)

    plt.title('Average Title Length by Store', fontsize=15)
    plt.xlabel('Store Name', fontsize=12)
    plt.ylabel('Average Number of Characters', fontsize=12)

    plt.show()

def most_expensive_popular_brands():
    branded_df = df[df['has_brand'] == 1].copy()

    top_10_names = branded_df['brand'].value_counts().nlargest(10).index
    top_10_df = branded_df[branded_df['brand'].isin(top_10_names)]

    sorted_brands = (
        top_10_df.groupby('brand')['price($)']
        .mean()
        .sort_values(ascending=False)
        .index
    )

    sns.set_style("whitegrid")
    plt.figure(figsize=(12, 7))
    plt.ylim(0, 1000)

    ax = sns.barplot(
        data=top_10_df,
        x='brand',
        y='price($)',
        order=sorted_brands,
        palette='viridis',
        capsize=.1
    )

    counts_map = top_10_df['brand'].value_counts()

    for i, p in enumerate(ax.patches):
        p: patches.Rectangle = p
        brand_name = sorted_brands[i]
        n_value = counts_map[brand_name]

        ax.annotate(f'n={n_value}',
                    (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center',
                    xytext=(0, 15),
                    textcoords='offset points',
                    fontsize=10, fontweight='bold')

    max_avg_price = top_10_df.groupby('brand')['price($)'].mean().max()
    plt.ylim(0, max_avg_price * 1.3)

    plt.title('Top 10 Most Frequent Brands Sorted by Average Price', fontsize=16)
    plt.xlabel('Brand Name', fontsize=12)
    plt.ylabel('Average Price ($)', fontsize=12)
    plt.xticks(rotation=30)

    plt.tight_layout()
    plt.show()

def most_expensive_announcements():
    top_10_expensive = df.nlargest(10, 'price($)')

    sns.set_style("whitegrid")
    plt.figure(figsize=(12, 8))

    ax = sns.barplot(
        data=top_10_expensive,
        x='price($)',
        y='title',
        palette='magma'
    )

    for p in ax.patches:
        p: patches.Rectangle = p
        width = p.get_width()
        ax.text(
            width + 10,
            p.get_y() + p.get_height() / 2,
            f'${width:,.2f}',
            va='center',
            fontsize=11,
            fontweight='bold'
        )

    plt.title('Top 10 Most Expensive Individual Listings', fontsize=16)
    plt.xlabel('Price ($)', fontsize=12)
    plt.ylabel('Listing Title', fontsize=12)

    ax.set_yticklabels([text.get_text()[:60] + '...' if len(text.get_text()) > 60 else text.get_text() for text in
                        ax.get_yticklabels()])

    plt.tight_layout()
    plt.show()

def get_IQR_bounds(data_frame, param):
    q1 = data_frame[param].quantile(0.25)
    q3 = data_frame[param].quantile(0.75)
    iqr = q3 - q1
    return q1 - 1.5 * iqr, q3 + 1.5 * iqr

def clean_outliers(input_df):
    working_df = input_df.copy()

    t_low, t_up = get_IQR_bounds(working_df, 'title_length')
    p_low, p_up = get_IQR_bounds(working_df, 'price($)')

    mask = (
        (working_df['title_length'] >= t_low) & (working_df['title_length'] <= t_up) &
        (working_df['price($)'] >= p_low) & (working_df['price($)'] <= p_up)
    )
    df_result = working_df[mask].copy()

    df_result['log_price'] = np.log1p(df_result['price($)'])
    df_result['log_title_length'] = np.log1p(df_result['title_length'])

    print(f"Removed: {len(working_df) - len(df_result)} rows")
    return df_result

def check_normal_dist_store(store_name):
    df_store = df[df['store_name'] == store_name].copy()
    df_store = clean_outliers(df_store)
    normal_dist_test_k2(df_store, 'log_title_length')
    qq_plot(df_store, 'log_title_length')
    normal_dist_test_k2(df_store, 'log_price')
    qq_plot(df_store, 'log_price')

cleaned_df = clean_outliers(df)
cleaned_df.to_csv('C:\\Users\\Musiyenko.M\\PycharmProjects\\leather_jackets_analysis\\analysis\\regression\\cleaned_df.csv')
