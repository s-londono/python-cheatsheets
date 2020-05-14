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

# How many articles each user interacts with in the dataset
df_article_x_user = df[["article_id", "email"]]
df_count_artices_x_user = df_article_x_user.groupby(by=["email"]).count()
df_count_artices_x_user.columns = ["count_articles"]

# Bunch of descriptive statistics
descript_stats = df_count_artices_x_user.describe(percentiles=[0.10, 0.25, 0.50, 0.75, 0.85, 0.95, 0.99])

df_count_artices_x_user["count_category"] = \
    df_count_artices_x_user["count_articles"].apply(lambda c: c if c < 40 else 45)

df_count_articles_low = df_count_artices_x_user[df_count_artices_x_user["count_articles"] < 40]

# Plot histogram
plt.hist(x=df_count_artices_x_user["count_category"], bins=20)
plt.title("Total articles read per user")
plt.show()

plt.boxplot(x=df_count_articles_low["count_articles"])
plt.title("Total articles read per user")
plt.show()
