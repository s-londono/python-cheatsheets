import nltk
from nltk.tokenize import word_tokenize
from nltk import pos_tag, ne_chunk

# nltk.download('words')
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('maxent_ne_chunker')

# POS Tagging the text

text = "I always lie down to tell a lie."

sentence = word_tokenize(text)
tags = pos_tag(sentence)

print(tags)

# Named Entity Recognition (NER)

text = "Antonio joined Udacity Inc. in California."
ner_tree = ne_chunk(pos_tag(word_tokenize(text)))

print(ner_tree)

# Sentence Parsing

# Define a custom grammar
my_grammar = nltk.CFG.fromstring("""
S -> NP VP
PP -> P NP
NP -> Det N | Det N PP | 'I'
VP -> V NP | VP PP
Det -> 'an' | 'my'
N -> 'elephant' | 'pajamas'
V -> 'shot'
P -> 'in'
""")

parser = nltk.ChartParser(my_grammar)

# Parse a sentence
sentence = word_tokenize("I shot an elephant in my pajamas")

for tree in parser.parse(sentence):
    tree.draw()
