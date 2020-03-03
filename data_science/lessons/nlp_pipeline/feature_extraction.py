# Three useful methods of vectorizing text:
# - CountVectorizer - Bag of Words
# - TfidfTransformer - TF-IDF values
# - TfidfVectorizer - Bag of Words AND TF-IDF values

import re
import nltk
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer

# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')

corpus = ["The first time you see The Second Renaissance it may look boring.",
          "Look at it at least twice and definitely watch part 2.",
          "It will change your view of the matrix.",
          "Are the human people the ones who started the war?",
          "Is AI a bad thing ?"]

stop_words = stopwords.words("english")
lemmatizer = WordNetLemmatizer()

# Apply:
# - Case normalization (convert to all lowercase)
# - Punctuation removal
# - Tokenization, lemmatization, and stop word removal using nltk


def tokenize(text):
    # Normalize case and remove punctuation
    text = re.sub(r"[^a-zA-Z0-9]", " ", text.lower())

    # Tokenize text, remove stop words and lemmatize
    tokens = word_tokenize(text)
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words]

    return tokens


# BAG-OF-WORDS: COUNT VECTORIZER

# Initialize count vectorizer object
vect = CountVectorizer(tokenizer=tokenize)

# Get counts of each token (word) in text data
X = vect.fit_transform(corpus)

# Convert sparse matrix to numpy array to view
X.toarray()

# view token vocabulary and counts
vect.vocabulary_

# TF-IDF

# Initialize tf-idf transformer object
transformer = TfidfTransformer(smooth_idf=False)

# Use counts from Count Vectorizer results to compute TF-IDF values
tfidf = transformer.fit_transform(X)

# Convert sparse matrix to numpy array to view
tfidf.toarray()

# TF-IDF Vectorizer
# TfidfVectorizer = CountVectorizer + TfidfTransformer
# This is just an abbreviated way to perform Bag of Words followed by TF-IDF transformations on the corpus

# Initialize tf-idf vectorizer object
vectorizer = TfidfVectorizer()

# Compute Bag of Word counts and TF-IDF values
X = vectorizer.fit_transform(corpus)

# Convert sparse matrix to numpy array to view. Should yield the same result as TF-IDF over Bag of Words
X.toarray()
