import json
from pdf_to_txt import pdf_to_text1
from stemm import stemming

f_name = './Linkedin/Abhishek Jain.pdf'
# give the name of json file to be created
def grouping():
    json_file = 'txt_with_header.json'
    headermqin = "personal"
    result = pdf_to_text1(f_name)
    header_keywords = ["experi","profession","employ","educ","academ","technolog","skill","strength","award","certif","honor","public"]
    print("++++++++++++++++",result)
    """
    experience --> experi,profession,employ
    education --> educ,academ
    skills --> technolog,skill,strength
    awards --> award,certif,honor,public

    incase personal details not found then take first 10 lines a personal details then proceed
    some times experience and skills are mixed up 
    """
    final_json =[]
    with open(json_file, 'w') as fp:
        for line in result:
            data = dict()
            #print(line)
            sentence = line
            if (sentence.strip("\n").strip() and sentence!="\u00a0\n" and sentence!="\f\u00a0\n" and sentence!="\f" and sentence!="\f"):
                if len(sentence.split()) < 5:
                    #print("sentence less than 4====",sentence)
                    for ele in header_keywords:
                        #print("these are the elements",ele,) 
                        #print("sdntence in lower",sentence.lower(),"fdaf")
                        sentence_lower = sentence.lower().strip()
                        stemmed_sentence = stemming(sentence_lower)
                        #print("type of ele",type(ele))
                        #print("type of check",type(sentence_lower))
                        if any(ele in s for s in stemmed_sentence):
                            if ele == "experi" or ele == "profession" or ele == "employ":
                            #print("match found****************************************")
                                headermqin = "Experience"
                            
                            elif ele == "educ" or ele == "academ": 
                                headermqin = "Education"

                            elif ele == "technolog" or ele == "skill" or ele == "strength":
                                headermqin = "Skill"

                            elif ele == "project" or ele == "assign":
                                headermqin = "Project"
                        
                            
                    
                data['text'] = sentence
                data['header'] = headermqin
                final_json.append(data)
        fp.write(json.dumps(final_json))
grouping()
