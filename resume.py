from flask import Flask, render_template, request
import spacy

app = Flask(__name__)

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/parse', methods=['POST'])
def parse_resume():
    if 'resume' not in request.files:
        return "No file part"
    
    resume = request.files['resume']
    
    if resume.filename == '':
        return "No selected file"
    
    text = resume.read().decode('utf-8')
    
    # Parse the resume using spaCy
    doc = nlp(text)
    
    # Extract relevant information (example: extracting skills)
    skills = extract_skills(doc)
    
    return render_template('result.html', skills=skills)

def extract_skills(doc):
    # Example: Extract skills by looking for entities tagged as 'ORG' (organizations)
    skills = []
    for ent in doc.ents:
        if ent.label_ == 'ORG':
            skills.append(ent.text)
    return skills

if __name__ == '__main__':
    app.run(debug=True)
