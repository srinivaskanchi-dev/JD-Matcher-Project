from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import spacy
import json

# Load spaCy English model (download with: python -m spacy download en_core_web_sm)
nlp = spacy.load('en_core_web_sm')

def compute_match_score(resume_text, jd_text):
    """Compute TF-IDF + Cosine Similarity between resume and job description."""
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf = vectorizer.fit_transform([resume_text, jd_text])
    score = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
    return round(score * 100, 2)  # Return as percentage

def extract_skills(text):
    """Extract skills and keywords using spaCy NER and simple rules."""
    doc = nlp(text)
    # Extract entities labeled as ORG, GPE, PERSON, etc. (customize as needed)
    entities = [ent.text for ent in doc.ents if ent.label_ in ['ORG', 'GPE', 'PERSON', 'PRODUCT', 'SKILL']]
    # Extract noun chunks as possible skills
    noun_chunks = [chunk.text for chunk in doc.noun_chunks]
    # Combine and deduplicate
    skills = list(set(entities + noun_chunks))
    return skills

def generate_ats_resume(resume_text, jd_text):
    """Generate an ATS-friendly resume by emphasizing skills/keywords from the JD."""
    jd_skills = extract_skills(jd_text)
    resume_lines = resume_text.splitlines()
    # Highlight or add JD skills to resume (simple approach)
    enhanced_resume = resume_text
    for skill in jd_skills:
        if skill.lower() not in resume_text.lower():
            enhanced_resume += f"\n- {skill} (from JD)"
    return enhanced_resume

def generate_interview_questions(resume_text, jd_text, num_questions=7):
    """Generate basic interview questions based on resume and JD keywords."""
    skills = extract_skills(resume_text + ' ' + jd_text)
    questions = [f"Can you tell us about your experience with {skill}?" for skill in skills[:num_questions]]
    return questions

def generate_explanation(resume_text, jd_text, match_score):
    """Generate a plain English explanation of the match."""
    if match_score > 80:
        level = "excellent"
    elif match_score > 60:
        level = "good"
    elif match_score > 40:
        level = "fair"
    else:
        level = "low"
    return (
        f"The resume matches the job description with a {level} score of {match_score}%. "
        "Key skills and experiences from the resume align with the job requirements. "
        "Consider tailoring your resume further for even better results."
    ) 