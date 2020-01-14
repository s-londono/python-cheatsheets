import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error
import seaborn as sns
import os

# Read dataset in DataFrame df
full_df = pd.read_csv("data-science/resources/survey_results_public.csv")
full_df.head()

# Initial exploration of the data. Summary statistics of Quantitative Variables and Histogram
full_df.describe()
full_df.hist()

# Get a correlation metric and render as a Heat Map
corr_mtx = full_df.corr()
sns.heatmap(corr_mtx, annot=True, fmt=".2f")

# Extract quantitative data (in this case ignore categorical data, because of the Linear Regression model)
df = full_df[['CareerSatisfaction', 'JobSatisfaction', 'HoursPerWeek', 'StackOverflowSatisfaction', 'Salary']]

# Deal with missing data. Scikit-learn models cannot work with datasets containing NaN values:

# - Option 1: Drop rows containing missing values (default arguments axis=0, how='any')
fixed_df = df.dropna()

# Get a list of Explanatory Variables, which will be used to predict the Response Variable.
# A good first guess is just to get all the Continuous Variables. Get the Response Variable too
X = fixed_df[['CareerSatisfaction', 'JobSatisfaction', 'HoursPerWeek', 'StackOverflowSatisfaction']]
y = fixed_df['Salary']

# Split the dataset into Training and Test sets. Here the test set size will be 30% of the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Instantiate the model. Usually it's necessary to normalize (standarize) the data. It's the safe thing to do
lm_model = LinearRegression(normalize=True)

# Fit the model to the training data
lm_model.fit(X_train, y_train)

# Predict on the test data
y_test_preds = lm_model.predict(X_test)

# R-squared value to measure how well the predicted values compare to the actual test values
r2_test = r2_score(y_test, y_test_preds)

# Score the model on the test data