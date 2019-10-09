import pandas as pd
import spacy
import re
from spacy.matcher import PhraseMatcher

nlp = spacy.load("en_core_web_lg")


def read_keywords(file):
    line = file.readline().strip()
    listOfKeywords = []
    while line:
        listOfKeywords.append(line)
        line = file.readline().strip()

    return listOfKeywords


def get_skills(text):
    with open("skills.txt", encoding="utf-8") as f:
        listOfKeywords = read_keywords(f)
    # nlp = spacy.load('en_core_web_sm')
    matcher = PhraseMatcher(nlp.vocab)
    patterns = [nlp.make_doc(text) for text in listOfKeywords]
    matcher.add("Skills", None, *patterns)
    doc = nlp(text)
    skills = set()
    skill = []

    matches = matcher(doc)
    for match_id, start, end in matches:
        span = doc[start:end]
        if span.text:
            skills.add(span.text)
    skill.append(skills)
    text1= ""
    #print(skills)
    for i in skills:
        print("iiii", i)
        text1 = text1 + i + "\n"
    doc = nlp(text1)
    print("textadfaf", text1)
    for entity in doc.ents:
        print(entity.text, entity.label_)

def name():
    df = pd.read_json('txt_with_header.json')
    df = df['text']
    text = ""
    for i in df:
        
        text = text + i + '\n'
    get_skills(text)
    #doc = nlp(text)
    #print("text", text)
    #for entity in doc.ents:
        #print(entity.text, entity.label_)

name()
