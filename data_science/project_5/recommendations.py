import os

if not os.getcwd().endswith("project_5"):
    os.chdir("data_science/project_5")

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle

df = pd.read_csv('data/user-item-interactions.csv')
df_content = pd.read_csv('data/articles_community.csv')
del df['Unnamed: 0']
del df_content['Unnamed: 0']

# Get an idea of the data (article titles and contents)
df_head = df.head()
df_content_head = df_content.head()

# PART I: EXPLORATORY DATA ANALYSIS

# 1. What is the distribution of how many articles a user interacts with in the dataset? Provide visual and
# descriptive statistics to assist with giving a look at the number of times each user interacts with an article

# The dataframe df_count_artices_x_user contains the number of articles each user interacted with
df_article_x_user = df[["article_id", "email"]]
df_num_user_interactions = df_article_x_user.groupby(by=["email"]).count()
df_num_user_interactions.columns = ["num_interactions"]

# Compute the usual descriptive statistics on the dataset. Include some quantiles of interest
descript_stats = df_num_user_interactions.describe(percentiles=[0.10, 0.25, 0.50, 0.75, 0.85, 0.95, 0.99])

# Get the median and maximum number of user_article interactios below
median_val = descript_stats.loc["50%", "num_interactions"]
max_views_by_user = descript_stats.loc["max", "num_interactions"]

print(f"50% of individuals interact with {median_val} number of articles or fewer.")
print(f"The maximum number of user-article interactions by any 1 user is {max_views_by_user}.")

# Take the number of interactions per user under 40 and set all the rest to 45.
# This view will make the histogram easier to read by cutting the long tail short
num_interactions_tailcut = df_num_user_interactions["num_interactions"].apply(lambda c: c if c < 40 else 45)

# Take the number of interactions per user under 40 and set all the rest to 45.
# This view will make the histogram easier to read by cutting the long tail short
num_interactions_tailcut = df_num_user_interactions["num_interactions"].apply(lambda c: c if c < 40 else 45)

plt.figure(figsize=(12, 5))

# Histogram of number of document interactions per user. Values above 40 stacked up at 45
plt.subplot(1, 2, 1)
plt.hist(x=num_interactions_tailcut, bins=45)
plt.title("Number of articles read per user")
import os

if not os.getcwd().endswith("project_5"):
    os.chdir("data_science/project_5")

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle

df = pd.read_csv('data/user-item-interactions.csv')
df_content = pd.read_csv('data/articles_community.csv')
del df['Unnamed: 0']
del df_content['Unnamed: 0']

# Get an idea of the data (article titles and contents)
df_head = df.head()
df_content_head = df_content.head()

# PART I: EXPLORATORY DATA ANALYSIS

# 1. What is the distribution of how many articles a user interacts with in the dataset? Provide visual and
# descriptive statistics to assist with giving a look at the number of times each user interacts with an article

# The dataframe df_count_artices_x_user contains the number of articles each user interacted with
df_article_x_user = df[["article_id", "email"]]
df_num_user_interactions = df_article_x_user.groupby(by=["email"]).count()
df_num_user_interactions.columns = ["num_interactions"]

# Compute the usual descriptive statistics on the dataset. Include some quantiles of interest
descript_stats = df_num_user_interactions.describe(percentiles=[0.10, 0.25, 0.50, 0.75, 0.85, 0.95, 0.99])

# Get the median and maximum number of user_article interactios below
median_val = descript_stats.loc["50%", "num_interactions"]
max_views_by_user = descript_stats.loc["max", "num_interactions"]

print(f"50% of individuals interact with {median_val} number of articles or fewer.")
print(f"The maximum number of user-article interactions by any 1 user is {max_views_by_user}.")

# Take the number of interactions per user under 40 and set all the rest to 45.
# This view will make the histogram easier to read by cutting the long tail short
num_interactions_tailcut = df_num_user_interactions["num_interactions"].apply(lambda c: c if c < 40 else 45)

# Take the number of interactions per user under 40 and set all the rest to 45.
# This view will make the histogram easier to read by cutting the long tail short
num_interactions_tailcut = df_num_user_interactions["num_interactions"].apply(lambda c: c if c < 40 else 45)

plt.figure(figsize=(12, 5))

# Histogram of number of document interactions per user. Values above 40 stacked up at 45
plt.subplot(1, 2, 1)
plt.hist(x=num_interactions_tailcut, bins=45)
plt.title("Number of articles read per user")

# Boxplot of number of document interactions per user
plt.subplot(1, 2, 2)
plt.boxplot(x=df_num_user_interactions["num_interactions"])
plt.title("Number of articles read per user")

plt.show()

# 2. Explore and remove duplicate articles from the df_content dataframe
print(f"Number of duplicate article IDs: {df_content.duplicated(subset=['article_id']).sum()}")
print(f"Number of duplicate article names: {df_content.duplicated(subset=['doc_full_name']).sum()}")
print(f"Number of duplicate article ID - names: {df_content.duplicated(subset=['doc_full_name', 'article_id']).sum()}")

# Remove any rows that have the same article_id - only keep the first
df_content.drop_duplicates(subset="article_id", keep="first", inplace=True)

# 3. Find:

# Get the IDs of the articles users interacted with
interacted_art_ids = df_article_x_user["article_id"].unique()

# a. The number of unique articles that have an interaction with a user
unique_articles = df_content['article_id'].isin(interacted_art_ids).sum()
# b. The number of unique articles in the dataset (whether they have any interactions or not)
total_articles = df_content['article_id'].nunique()
# c. The number of unique users in the dataset. (excluding null values)
unique_users = df[df['email'].notna()]['email'].nunique()
# d. The number of user-article interactions in the dataset.
user_article_interactions = len(df.groupby(by=['article_id', 'email']).groups)
