from nltk.tag import StanfordNERTagger
import pandas as pd
import spacy
nlp = spacy.load("en_core_web_sm")
import nltk


def name_nltk(text):
    import nltk


st = StanfordNERTagger('/usr/share/stanford-ner/classifiers/english.all.3class.distsim.crf.ser.gz',
                       '/usr/share/stanford-ner/stanford-ner.jar',
                       encoding='utf-8')

for sent in nltk.sent_tokenize(text):
    tokens = nltk.tokenize.word_tokenize(sent)
    tags = st.tag(tokens)
    for tag in tags:
        if tag[1]=='PERSON': print (tag)

def get_name_and_confidence_level(text):
    if type(text) != str:
        text = str(text)

    answer_doc = nlp(text)

    proper_nouns = []
    common_nouns = []
    adjectives = []
    adverbs = []
    references = []
    # for token in answer_doc:
    #     print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,token.shape_, token.is_alpha, token.is_stop)
    for num, token in enumerate(answer_doc):
        if token.is_stop is False:
            if token.tag_ in ["NNP", "NNPS"] and token.dep_ in ["attr", "ROOT", "acomp", "compound", "nsubj", "oprd", "appos", "npadvmod"]:
                if token.text.lower() not in ["name", "impress"]:
                    proper_nouns.append(token.text)

            elif token.tag_ in ["NN", "NNS"] and token.dep_ in ["attr", "ROOT", "acomp"]:
                if token.text.lower() not in ["name", "impress"] and token.dep_ not in ["pobj"]:
                    common_nouns.append(token.text)

            elif token.tag_ in ["JJ"]:
                if token.dep_ not in ["pobj"]:
                    adjectives.append(token.text)

            elif token.tag_ in ["RB"]:
                if token.dep_ not in ["pobj"]:
                    adjectives.append(token.text)

        references.append(token.tag_)

    if proper_nouns:
        confidence_level = 3
        first_name = " ".join(proper_nouns)
    elif common_nouns:
        confidence_level = 3
        first_name = " ".join(common_nouns)
    elif adjectives:
        confidence_level = 2
        first_name = " ".join(adjectives)
    elif adverbs:
        confidence_level = 1
        first_name = " ".join(adverbs)
    else:
        confidence_level = 0
        first_name = text
    return first_name


def name():
    df = pd.read_json('txt_with_header.json')
    df_personal = df['text'][df['header'] == 'personal']
    if df_personal.empty:
        df_personal = df.loc[:10, 'text']
    df_name = df.loc[:5, 'text']
    text = ""
    for i in df_name:
        text = text + i + '\n'
    text1 = ""
    for i in df_personal:
        text1 = text1 + i + '\n'
    #name_nltk(text1)
    
    """doc = nlp(text)
    for entity in doc.ents:
        print(entity.text, entity.label_)
    for entity in doc.ents:
        if entity.label_ == "PERSON" or entity.label_ == "ORG":
                if not entity.text.strip():
                    continue
                print(entity.text.strip())
                name = entity.text.split()
                if len(name) > 1:
                    print("first name ", name[0])
                    print("last name", name[1])
                else:
                    print("first name", name[0])
                break"""
    name = get_name_and_confidence_level(text)
    print("name---",name)
    """name = name.split()
    print("first_name :", name[0])
    print("last_name :", name[1])"""

    print("++++++++")
    
    name_check = df.loc[:0, 'text'].values[0]
    name_check = name_check.lstrip(' ')
    name1 = name_check.split(" ",1)
    
    #print("first_name :", name1[0])
    #print("last_name :", name1[1])




name()
