import spacy
import nltk

from nltk.stem.porter import *

stemmer = PorterStemmer()
nlp = spacy.load("en_core_web_md")

def stemming(data):
    doc2 = nlp(data)
    stemmed_data = list()
    for token in doc2:
        stemmed_data.append(stemmer.stem(token.text))
    return stemmed_data