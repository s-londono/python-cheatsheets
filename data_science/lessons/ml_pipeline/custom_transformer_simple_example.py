# Implement a custom transformer by extending the base class in Scikit-Learn.
# Remember, all estimators have a fit method, and since this is a transformer,
# it also has a transform method

# Another way to create custom transformers is by using this FunctionTransformer from scikit-learn's
# preprocessing module. This allows you to wrap an existing function to become a transformer.
# This provides less flexibility, but is much simpler
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


class TenMultiplier(BaseEstimator, TransformerMixin):
    """
    This is a very simple Transformer that multiplies the input data by ten
    """
    def __init__(self):
        pass

    def fit(self, x, y=None):
        """
        Takes in a 2d array X for the feature data and a 1d array y for the target labels. Inside the fit method,
        we simply return self. This allows us to chain methods together, since the result on calling fit on the
        transformer is still the transformer object. This method is required to be compatible with scikit-learn
        """
        return self

    def transform(self, x):
        """
        The transform function is where we include the code that well, transforms the data. In this case, we return
        the data in X multiplied by 10. This transform method also takes a 2d array X
        """
        return x * 10


# Simple test
X = np.array([6, 3, 7, 4, 7])
multiplier = TenMultiplier()
print(multiplier.transform(X))


class CaseNormalizer(BaseEstimator, TransformerMixin):
    """
    Let's build a case normalizer, which simply converts all text to lowercase. We aren't setting anything
    in our init method, so we can actually remove that
    """
    def fit(self, x, y=None):
        return self

    def transform(self, x):
        """
        We can lowercase all the values in X by applying a lambda function that calls lower on each value.
        We'll have to wrap this in a pandas Series to be able to use this apply function
        """
        return pd.Series(X).apply(lambda x: x.lower()).values


# Simple test
X = np.array(['Implementing', 'a', 'Custom', 'Transformer', 'from', 'SCIKIT-LEARN'])
case_normalizer = CaseNormalizer()
print(case_normalizer.transform(X))
