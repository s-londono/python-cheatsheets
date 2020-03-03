import re
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer

# nltk.download('stopwords')
# nltk.download('wordnet') # download for lemmatization

text = "The first time you see The Second Renaissance it may look boring. Look at it at least twice and definitely " \
       "watch part 2. It will change your view of the matrix. Are the human people the ones who started the war ? Is " \
       "AI a bad thing ? "

# Normalize text
text = re.sub(r"[^a-zA-Z0-9]", " ", text.lower())

# Tokenize text
words = text.split()
print(words)

# Remove stop words
words = [w for w in words if w not in stopwords.words("english")]

# Lemmatizing

# Reduce words to their root form
lemmed = [WordNetLemmatizer().lemmatize(w) for w in words]
print(lemmed)

# Lemmatize verbs by specifying pos
print(words)

# Stemming

# Reduce words to their stems
stemmed = [PorterStemmer().stem(w) for w in words]
print(stemmed)
lemmed = [WordNetLemmatizer().lemmatize(w, pos='v') for w in lemmed]
print(lemmed)
