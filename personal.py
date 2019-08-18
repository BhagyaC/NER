from spacy.matcher import PhraseMatcher
import re
import spacy
nlp = spacy.load("en_core_web_sm")


REGEX_EMAIL = r'([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})'
REGEX_PHONE = r'(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}'
REGEX_URL = r'(https?:\/\/)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)'
REGEX_EMAIL_LABEL = r'E:|Email:?|email:?|'
REGEX_PHONE_LABEL = r'M:|Mobile:?|Phone:?|Tel:|Tel.|Telephone:?|Cell:|Cellphone:?'
REGEX_ADDRESS_LABEL = r'Address:?|ADDRESS:?'
REGEX_URL_LABEL = r'Url:|Website:?'


# @bhagya method is not used
def addPipeToMatch(match):
    return "|" + match.group(1)


def replace_with_space(match):
    return " " + match.group(2)


def read_keywords(file):
    line = file.readline().strip()
    list_of_keywords = []
    while line:
        # line.replaceAll("^\"|\"$", "")
        list_of_keywords.append(line.lower())
        line = file.readline().strip()
    # print(list_of_keywords)

    return list_of_keywords


def replace_regex_with_text(text, list_of_regex, replacement):
    for regex in list_of_regex:
        text = re.sub(regex, replacement, text)
    return text


def preProcessText(text):
    text = text.encode("ascii", "ignore").decode()
    text = re.sub(r"-\n{1,2}", "", text)
    text = re.sub(
        r"(\n{2,}|\s{3,}|\t+|\r{2,}| {3,}|\f+|\v+)([a-z])", replace_with_space, text)
    print ("preprocessed text",text )
    return text


def get_address_from_text(text):
    text = preProcessText(text)
    print("preprocessed ",text)
    address_list = list()
    add_list = list()
    regex_pattern = r"\n{2,}|\s{2,}|\t+|\r{2,}| {2,}|\f+|\v+|\|"
    newLineSeparatedList = re.split(
        regex_pattern, text)
    for new_line_separated_section in newLineSeparatedList:
        print("new line",new_line_separated_section)
        doc = nlp(new_line_separated_section)
        is_break = False
        gpe_count = 0
        for entity in doc.ents:
            if entity.label_ == "GPE":
                add_list.append(str(entity))
                print("entity",entity)
                gpe_count += 1
                if gpe_count > 0:
                    new_line_separated_section = replace_regex_with_text(new_line_separated_section, [
                        REGEX_EMAIL, REGEX_PHONE, REGEX_URL, REGEX_EMAIL_LABEL, REGEX_PHONE_LABEL, REGEX_ADDRESS_LABEL,
                        REGEX_URL_LABEL], "")
                    address_list.append(new_line_separated_section)
                    is_break = True
                    break
        if is_break:
            break
    '''if len(address_list)==0:
        return add_list
    else:'''
    return address_list


def languages_known(text):
    # text=text.replace("\n","")

    text = text.replace("\uf0b7", "")
    text = text.lower()
    # print(text)
    with open("language.txt", encoding="utf-8") as f:
        list_of_keywords = read_keywords(f)
    matcher = PhraseMatcher(nlp.vocab)
    patterns = [nlp.make_doc(text) for text in list_of_keywords]
    matcher.add("lang", None, *patterns)
    doc = nlp(text)
    result = []
    matches = matcher(doc)
    if matches:
        for match_id, start, end in matches:
            span = doc[start:end]
            result.append(span.text)
    return result


def extract_website(text):
    website_list = list()
    ws = {}
    website = re.search(
        REGEX_URL, text)
    if website:
        # ws["type"] = "website"
        ws["url"] = website.group()
    website_list.append(ws)
    return website_list


def extract_personal_info(text, nlp):
    # text = text[:200]
    personalInfo = {}
    doc = nlp(text)
    for entity in doc.ents:
        if entity.label_ == "PERSON" or entity.label_ == "ORG":
            if not entity.text.strip():
                continue
            personalInfo["FirstName"] = entity.text.strip()
            personalInfo['LastName'] = entity.text.strip()
            text = re.sub(personalInfo["FirstName"], "", text)
            text = re.sub(personalInfo['LastName'], "", text)
    
            break
    mobileNo = re.search(
        r'(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}', text)
    if mobileNo:
        personalInfo["Phone"] = mobileNo.group()
    emailId = re.search(
        r'([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})', text)
    if emailId:
        personalInfo["Email"] = emailId.group()
    text = re.sub(REGEX_EMAIL, "", text)
    text = re.sub(REGEX_PHONE , "", text)
    
    
    for ent in doc.ents:
        #logger.debug('ent.text: {}'.format(ent.text))
        #logger.debug('ent.start_char: {}'.format(ent.start_char))
        #logger.debug('ent.end_char: {}'.format(ent.end_char))
        #logger.debug('ent.label_: {}'.format(ent.label))
        print('ent.text: {}'.format(ent.text))

        if ent.label_ == "DATE":
            personalInfo["DOB"] = ent.text
    personalInfo["Address"] = get_address_from_text(text)
    #personalInfo["languages"] = languages_known(text)
    personalInfo["website"] = extract_website(text)
    # print(personalInfo)
    return personalInfo


def personal_info(text):
    #logger.debug('Running NER for personal info.')
    # df1 = pd.read_json(filename)
   
    info = extract_personal_info(text, nlp)
    #logging.debug('NER Personal Info result: {}'.format(info))
    return info