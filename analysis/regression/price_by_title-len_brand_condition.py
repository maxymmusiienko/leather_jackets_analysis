import statsmodels.api as sm
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

df = pd.read_csv('C:\\Users\\Musiyenko.M\\PycharmProjects\\leather_jackets_analysis\\analysis\\regression\\cleaned_df.csv')

X = df[['log_title_length', 'has_brand', 'simple_condition']].copy()

X = pd.get_dummies(X, columns=['simple_condition'], drop_first=True)

X = sm.add_constant(X)

y = df['log_price']

model = sm.OLS(y, X.astype(float))
results = model.fit()

print(results.summary())

plt.figure(figsize=(10, 6))
sns.residplot(x=results.fittedvalues, y=results.resid, lowess=True, line_kws={'color': 'red'})
plt.title('Residuals vs Fitted Values', fontsize=15)
plt.xlabel('Predicted Log Price', fontsize=12)
plt.ylabel('Residuals', fontsize=12)
plt.show()

plt.figure(figsize=(8, 6))
correlation_matrix = X.drop('const', axis=1).join(y).corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Correlation Matrix of Regression Features')
plt.show()
