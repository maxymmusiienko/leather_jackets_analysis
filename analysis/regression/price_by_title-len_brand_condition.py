import statsmodels.api as sm
import pandas as pd

df = pd.read_csv('C:\\Users\\Musiyenko.M\\PycharmProjects\\leather_jackets_analysis\\analysis\\regression\\cleaned_df.csv')

X = df[['log_title_length', 'has_brand', 'simple_condition']].copy()

X = pd.get_dummies(X, columns=['simple_condition'], drop_first=True)

X = sm.add_constant(X)

y = df['log_price']

model = sm.OLS(y, X.astype(float))
results = model.fit()

print(results.summary())
