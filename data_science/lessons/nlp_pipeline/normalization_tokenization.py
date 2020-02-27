import re
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords

# Download NLTK components if haven't done so
# nltk.download('punkt')
# nltk.download('stopwords')

print(stopwords.words("english"))

text = "The first time you see The Second Renaissance it may look boring. Look at it at least twice and definitely " \
       "watch part 2. It will change your view of the matrix. Are the human people the ones who started the war ? Is " \
       "AI a bad thing ? "

print(text)

# Normalize text
text = text.lower()
text = re.sub(r"[^0-9a-zA-Z]", " ", text)

# Tokenize text
words = word_tokenize(text)
print(words)

# Remove stop words
words = [w for w in words if w not in stopwords.words("english")]
print(words)

# Note that the sentence tokenizer is also provided by NLTK
text2 = "The first time you see The Second Renaissance it may look boring. Look at it at least twice and definitely " \
        "watch part 2. It will change your view of the matrix. Are the human people the ones who started the war ? " \
        "Is AI a bad thing ? "

sentences = sent_tokenize(text2)
print(sentences)
