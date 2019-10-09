import pandas as pd
import spacy
import re
nlp = spacy.load("en_core_web_lg")


def addPipeToMatch(match):
    return "|" + match.group(1)


def replaceWithSpace(match):
    return " " + match.group(2)


def read_keywords(file):
    line = file.readline().strip()
    listOfKeywords = []
    while line:
        #line.replaceAll("^\"|\"$", "")
        listOfKeywords.append(line.lower())
        line = file.readline().strip()
    #print(listOfKeywords)

    return listOfKeywords


def replaceRegexWithText(text, listOfRegex, replacement):
    for regex in listOfRegex:
        text = re.sub(regex, replacement, text)
    return text


def preProcessText(text):
    text = text.encode("ascii", "ignore").decode()
    text = re.sub(r"-\n{1,2}", "", text)
    text = re.sub(
        r"(\n{2,}|\s{3,}|\t+|\r{2,}| {3,}|\f+|\v+)([a-z])", replaceWithSpace, text)
    return text
def address(text):
    REGEX_EMAIL = r'([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})'
    REGEX_PHONE = r'(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}'
    REGEX_URL = r'(https?:\/\/)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)'
    REGEX_EMAIL_LABEL = r'E:|Email:?|email:?|'
    REGEX_PHONE_LABEL = r'M:|Mobile:?|Phone:?|Tel:|Tel.|Telephone:?|Cell:|Cellphone:?'
    REGEX_ADDRESS_LABEL = r'Address:?|ADDRESS:?'
    REGEX_URL_LABEL = r'Url:|Website:?'

    text = preProcessText(text)
    address_list = list()
    regexPattern = r"\n{2,}|\s{2,}|\t+|\r{2,}| {2,}|\f+|\v+|\|"
    newLineSeparatedList = re.split(
        regexPattern, text)
    for newLineSeparatedSection in newLineSeparatedList:
        doc = nlp(newLineSeparatedSection)
        isBreak = False
        gpeCount = 0
        for entity in doc.ents:
            if entity.label_ == "GPE":
                print("gpe found and count",entity.text,gpeCount)
                gpeCount += 1
                if gpeCount == 2:
                    newLineSeparatedSection = replaceRegexWithText(newLineSeparatedSection, [
                        REGEX_EMAIL, REGEX_PHONE, REGEX_URL, REGEX_EMAIL_LABEL, REGEX_PHONE_LABEL, REGEX_ADDRESS_LABEL, REGEX_URL_LABEL], "")
                    address_list.append(newLineSeparatedSection)
                    isBreak = True
                    break
        if(isBreak):
            break

    return address_list


def name():
    df = pd.read_json('txt_with_header.json')
    df_personal = df['text'][df['header'] == 'personal']
    if df_personal.empty:
        print("there is no personal field")
        df_personal = df.loc[:10, 'text']
    df_name = df.loc[:5, 'text']
    text = ""
    for i in df_name:
        text = text + i + '\n'
    text1 = ""
    for i in df_personal:
        text1 = text1 + i + '\n'
    #name_nltk(text1)
    ad = address(text1)
    print("address",ad)
    doc = nlp(text1)
    print("text",text1)
    for entity in doc.ents:
        print(entity.text, entity.label_)
    for entity in doc.ents:
        if entity.label_ == "PERSON" or entity.label_ == "ORG":
                if not entity.text.strip():
                    continue
                print(entity.text.strip())
                name = entity.text.split(" ",1)
                if len(name) > 1:
                    print("first name ", name[0])
                    print("last name", name[1])
                else:
                    print("first name", name[0])
                break

name()
