import spacy
from spacy.lemmatizer import Lemmatizer
from spacy.lang.en import LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES
import nltk

from nltk.stem.porter import *

stemmer = PorterStemmer()

from nltk.stem.snowball import SnowballStemmer

stemmer2 = SnowballStemmer(language='english')




nlp = spacy.load("en_core_web_md")

doc = nlp(u"Professional Experience Industrial Experience Research Experience Technical Experience Relevant Experience Professional Development Work Experience Professional Profile Professional Background Professional Employment ")
doc2 =nlp(u"Computer Skills Statistical Packages Software Knowledge Technical Skills Core/Key Competencies(separate header - incase skills and core competencies, both exists in the resume) Summary of skills Computer Skills Key Skills Technical Strengths Technical Background Tools Technology ")
doc3 = nlp(u"Publications / Awards Honors Certifications Awards and Recognitions")
"""for chunk in doc.noun_chunks:
    print(chunk.text, chunk.root.text, chunk.root.dep_, chunk.root.head.text)
for token in doc:
    print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
            token.shape_, token.is_alpha, token.is_stop)


for word in doc:
    print(word.text,word.pos_,word.dep_)
for entity in doc.ents:
    print(entity)

for noun in doc.noun_chunks:
    print(noun.text)"""

for token in doc3:
    print(token.text + ' --> ' + stemmer.stem(token.text))
    print(token.text + '2 --> ' + stemmer2.stem(token.text))