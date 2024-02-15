import spacy

from PyPDF2 import PdfReader
from spacy.lang.en.stop_words import STOP_WORDS

# Load embedding.
nlp = spacy.load('en_core_web_md')

# Define skill and education path.
ruler_path = "education_skills.jsonl"

# We need to set overwite ents to true otherwise there will be some conflict with
# existing entity ruler from spacy. e.g. spacy think that phd is org.
config = {'overwrite_ents': True}
ruler = nlp.add_pipe("entity_ruler", config=config)
ruler.from_disk(ruler_path)


# Function to clean the input data.
def preprocessing(sentence):
    stopwords = list(STOP_WORDS)
    doc = nlp(sentence)
    cleaned_tokens = []

    for token in doc:
        if token.text not in stopwords and token.pos_ != 'PUNCT' and token.pos_ != 'SPACE' and \
                token.pos_ != 'SYM':
            cleaned_tokens.append(token.lemma_.lower().strip())

    return " ".join(cleaned_tokens)

# Just function to remove duplicate.
def unique_skills(x):
    return list(set(x))

# Just put get skills and get_education that we did in part 1 together with some
# Sorting fucntion.
def resume_parser(resume):
    reader = PdfReader(resume)
    n_page = len(reader.pages)
    output = ''
    for i in range(n_page):
        page = reader.pages[i]
        output += page.extract_text()

    #pass the text to the nlp
    output = preprocessing(output)
    doc = nlp(output)  #note that this nlp already know skills
    
    education = []
    skills = []
    
    #look at the ents
    for idx, ent in enumerate(doc.ents):
        #if the ent.label_ is SKILL, then we append it together with education e.g. Master in Data science
        if ent.label_ == "EDUCATION":
            try:  # If the next entity from education is skills use that as the degree name, not best practice but good enough.
                if doc.ents[idx + 1].label_ == 'SKILL': # Check if the next word is skill
                    temp = ent.text + ' in ' + doc.ents[idx + 1].text # if it is combine them e.g. 'Master' +'in' + 'data science'
                    education.append(temp)
                else:
                    education.append(ent.text)
            except:
                education.append(ent.text)

        if ent.label_ == "SKILL":
            skills.append(ent.text)
    # Remove duplicate
    skills = unique_skills(skills)
    # Descending sort

    return {'skills':skills, 'education':education}