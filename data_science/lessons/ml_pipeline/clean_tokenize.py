import os
import re
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer

# nltk.download(['punkt', 'wordnet'])

if not os.getcwd().endswith("ml_pipeline"):
    os.chdir("./data_science/lessons/ml_pipeline")


# Before we can classify any posts, we'll need to clean and tokenize the text data.


def load_data():
    df = pd.read_csv('data/corporate_messaging.csv', encoding='latin-1')
    df = df[(df["category:confidence"] == 1) & (df['category'] != 'Exclude')]
    X = df.text.values
    y = df.category.values
    return X, y


# Tokenize function does:
# 1. Identify any urls in text, and replace each one with the word, "urlplaceholder".
# 2. Split text into tokens.
# 3. For each token: lemmatize, normalize case, and strip leading and trailing white space.
# 4. Return the tokens in a list!
url_regex = r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"


def tokenize(text):
    # get list of all urls using regex
    detected_urls = re.findall(url_regex, text)

    # replace each url in text string with placeholder
    for url in detected_urls:
        text = text.replace(url, "urlplaceholder")

    # tokenize text
    tokens = word_tokenize(text)

    # initiate lemmatizer
    lemmatizer = WordNetLemmatizer()

    # iterate through each token
    clean_tokens = []
    for tok in tokens:
        # lemmatize, normalize case, and remove leading/trailing white space
        clean_tok = lemmatizer.lemmatize(tok).lower().strip()
        clean_tokens.append(clean_tok)

    return clean_tokens


# test out function
X, y = load_data()
for message in X[:5]:
    tokens = tokenize(message)
    print(message)
    print(tokens, '\n')
