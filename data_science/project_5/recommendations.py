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

# How many articles each user interacts with in the dataset
df_article_x_user = df[["article_id", "email"]]
df_count_artices_x_user = df_article_x_user.groupby(by=["email"]).count()

df_count_artices_x_user.plot(kind="hist")
plt.title("Total articles read by user")

