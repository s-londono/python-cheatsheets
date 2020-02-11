import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from sklearn.preprocessing import StandardScaler
import seaborn as sns
import os

# Read dataset in DataFrame df
full_df = pd.read_csv("data_science/resources/survey_results_public.csv")
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

# - Option 2: Impute
# drop_target_df = df.dropna(subset=['Salary'])
# imputed_df = df.apply(lambda col: col.fillna(col.mean()), axis=0)

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

# Score the model on the test data
# R-squared value to measure how well the predicted values compare to the actual test values
r2_test = r2_score(y_test, y_test_preds)

# CATEGORICAL VARIABLES

# Create dummy columns. Use the dummy_na argument to create an extra variable for NaNs
dummy_cols_df = pd.get_dummies(df['categorical_column'], dummy_na=True)

# Create a copy of the dataframe
cat_df_copy = cat_df.copy()
# Pull a list of the column names of the categorical variables
cat_cols_lst = cat_df.columns


def clean_data(df):
    """
    INPUT
    df - pandas dataframe

    OUTPUT
    X - A matrix holding all of the variables you want to consider when predicting the response
    y - the corresponding response vector

    This function cleans df using the following steps to produce X and y:
    1. Drop all the rows with no salaries
    2. Create X as all the columns that are not the Salary column
    3. Create y as the Salary column
    4. Drop the Salary, Respondent, and the ExpectedSalary columns from X
    5. For each numeric variable in X, fill the column with the mean value of the column.
    6. Create dummy columns for all the categorical variables in X, drop the original columns
    """
    # Drop rows with missing salary values
    df = df.dropna(subset=['Salary'], axis=0)
    y = df['Salary']

    # Drop respondent and expected salary columns
    df = df.drop(['Respondent', 'ExpectedSalary', 'Salary'], axis=1)

    # Fill numeric columns with the mean
    num_vars = df.select_dtypes(include=['float', 'int']).columns
    df[num_vars] = df[num_vars].apply(lambda c: c.fillna(c.mean()))

    # Dummy the categorical variables
    cat_vars = df.select_dtypes(include=['object']).copy().columns

    # WATCH OUT! drop_first has an enormous impact on the results!!!
    df = pd.get_dummies(df, prefix=cat_vars, columns=cat_vars, drop_first=True)

    X = df
    return X, y


# Use the function to create X and y
X, y = clean_data(df)


def coef_weights(coefficients, X_train):
    '''
    INPUT:
    coefficients - the coefficients of the linear model
    X_train - the training data, so the column names can be used
    OUTPUT:
    coefs_df - a dataframe holding the coefficient, estimate, and abs(estimate)

    Provides a dataframe that can be used to understand the most influential coefficients
    in a linear model by providing the coefficient estimates along with the name of the
    variable attached to the coefficient.
    '''
    coefs_df = pd.DataFrame()
    coefs_df['est_int'] = X_train.columns
    coefs_df['coefs'] = lm_model.coef_
    coefs_df['abs_coefs'] = np.abs(lm_model.coef_)
    coefs_df = coefs_df.sort_values('abs_coefs', ascending=False)
    return coefs_df


# Use the function
coef_df = coef_weights(lm_model.coef_, X_train)

# A quick look at the top results
coef_df.head(20)

# SCALE FEATURES IN A PANDAS DATAFRAME

sc_X = StandardScaler()
X_train = sc_X.fit_transform(X_train)
X_test = sc_X.transform(X_test)
sc_y = StandardScaler()
arr_y_train_scaled = sc_y.fit_transform(y_train.values.reshape(-1, 1))
y_train.iloc[:] = arr_y_train_scaled.squeeze()

# IMPORTANT! Remember to scale back predictions
y_test_preds = sc_y.inverse_transform(lm_model.predict(X_test))
