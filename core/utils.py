from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import spacy
import json
import os
from dotenv import load_dotenv
import aiohttp

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")

try:
    nlp = spacy.load('en_core_web_sm')
except OSError:
    print("SpaCy model 'en_core_web_sm' not found. Please run: python -m spacy download en_core_web_sm")
    nlp = None

def compute_match_score(resume_text, jd_text):
    if not resume_text or not jd_text:
        return 0.0
    vectorizer = TfidfVectorizer(stop_words='english')
    try:
        tfidf = vectorizer.fit_transform([resume_text, jd_text])
        score = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
        return round(score * 100, 2)
    except ValueError:
        print("ValueError in compute_match_score: Texts might be too short or lack meaningful content.")
        return 0.0

def extract_skills(text):
    if nlp is None:
        print("SpaCy model not loaded, cannot extract skills.")
        return []
    doc = nlp(text)
    entities = [ent.text.lower() for ent in doc.ents if ent.label_ in ['ORG', 'GPE', 'PERSON', 'PRODUCT', 'SKILL']]
    noun_chunks = [chunk.text.lower() for chunk in doc.noun_chunks]
    skills = list(set(entities + noun_chunks))
    return skills

async def call_gemini_api(prompt, model="gemini-2.0-flash", temperature=0.7, max_tokens=2000, response_schema=None):
    chat_history = []
    chat_history.append({"role": "user", "parts": [{"text": prompt}]})

    payload = {"contents": chat_history}
    if response_schema:
        payload["generationConfig"] = {
            "responseMimeType": "application/json",
            "responseSchema": response_schema
        }

    apiKey = GOOGLE_API_KEY
    apiUrl = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={apiKey}"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(apiUrl, headers={'Content-Type': 'application/json'}, json=payload) as response:
                response.raise_for_status()
                result = await response.json()
                if result.get('candidates') and result['candidates'][0].get('content') and result['candidates'][0]['content'].get('parts'):
                    content = result['candidates'][0]['content']['parts'][0]['text']
                    if response_schema:
                        return json.loads(content)
                    return content
                else:
                    print(f"Gemini API did not return expected content: {result}")
                    return None
    except aiohttp.ClientError as e:
        print(f"Gemini API Client Error: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Gemini API JSON Decode Error: {e}")
        return None
    except Exception as e:
        print(f"General Error during Gemini API call: {e}")
        return None

async def generate_ats_resume(resume_text, jd_text):
    """
    Generates an ATS-friendly resume by using Google Gemini 2.0 Flash to rewrite
    the original resume, emphasizing keywords and experiences from the job description.
    The output will be in a structured plain text format for easier parsing.
    Explicitly asks for a concise resume, ideally fitting on one to two pages,
    and strictly avoids Python-like dictionary output.
    """
    prompt = f"""
    You are an expert resume writer and an ATS (Applicant Tracking System) specialist.
    Your task is to take a given resume and a job description, and then rewrite the resume
    to be highly optimized for ATS, ensuring it highlights the most relevant skills,
    experiences, and keywords from the job description. The rephrasing should focus on
    integrating the keywords from the job description naturally into the resume's content.

    **Crucially, keep the resume concise, aiming for a length that would typically fit on one to two pages.**
    **IMPORTANT: Do NOT include any Python-like dictionary structures (e.g., {{'type': 'paragraph', 'content': '...'}}) in the output.**
    **Output ONLY plain text, formatted as described below.**
    **if no relevant experience is found in parsed resume then make a section as as Pofessional Training or Internships**

    Output the rewritten resume in a structured plain text format using "SECTION: Section Name" for major headings.
    Use bullet points for lists within sections, denoted by a hyphen "- ".

    Ensure the following sections are present if applicable:
    SECTION: Contact Information
    SECTION: Summary
    SECTION: Experience
    SECTION: Education
    SECTION: Skills
    SECTION: Projects
    SECTION: Certifications
    SECTION: Awards (if any)

    SECTION: Contact Information  
    Format it like this:  
    Full Name (in UPPERCASE)  
    City, State, Country | Phone | Email  
    LinkedIn - <link> | GitHub - <link>

    Example Format:
    SECTION: Contact Information
    RAHUL DRAVID  
    Bangalore, Karnataka, India | +91-7256745365 | rahuldravid54@gmail.com  
    LinkedIn - www.linkedin.com/in/rahuldravid | GitHub - www.github.com/rahuldravid

    SECTION: Summary  
    Brief 2–4 line career summary, job-relevant.

    SECTION: Experience  
    Company Name | Location  
    Job Title | Dates  
-   Use bullet points to highlight key responsibilities and achievements.

    SECTION: Education
    Degree  
    Institute Name | Location
    Year of Graduation | GPA (if applicable)

    SECTION: Skills  
    Organize this in a labeled, grouped format, such as:  
    Programming Languages: Python, JavaScript, SQL  
    Web Development: Django, HTML5, CSS3, Bootstrap, REST APIs  
    Database Systems: MySQL (CRUD, optimization)  
    Version Control: Git, GitHub  
    Tools & Platforms: VS Code, Python IDLE, MS Office  
    Software Engineering: OOP, SDLC, Agile/Scrum, Debugging  
    Soft Skills: Logical Reasoning, Communication, Team Collaboration, Adaptability  

    SECTION: Projects (if applicable)  
    SECTION: Certifications (if any)  
    SECTION: Awards or Training (if any)

    ---
    Original Resume:
    {resume_text}

    ---
    Job Description:
    {jd_text}

    ---
    Rewritten ATS-Optimized Resume:
    """
    ats_resume_content = await call_gemini_api(prompt, temperature=0.7, max_tokens=2000)
    if ats_resume_content:
        return ats_resume_content
    return resume_text + "\n\n--- ATS Optimization Failed: Could not generate ATS resume. ---"

async def generate_interview_questions(resume_text, jd_text, num_questions=7):
    """
    Generates relevant interview questions based on the resume and job description
    using Google Gemini 2.0 Flash.
    """
    prompt = f"""
    You are an HR interviewer. Based on the following ATS-optimized resume and job description,
    generate {num_questions} insightful interview questions that assess the candidate's
    suitability for the role. Focus on behavioral, technical, and situational questions.
    Return the questions as a numbered list.

    ---
    ATS-Optimized Resume:
    {resume_text}

    ---
    Job Description:
    {jd_text}

    ---
    Interview Questions:
    """
    questions_text = await call_gemini_api(prompt, temperature=0.5, max_tokens=500)
    if questions_text:
        questions = [q.strip() for q in questions_text.split('\n') if q.strip()]
        return questions
    return ["Could not generate interview questions due to an error."]

def generate_explanation(match_score):
    """
    Generates a plain English explanation of the match score.
    """
    if match_score > 80:
        level = "excellent"
        detail = "Your resume aligns exceptionally well with the job description. You possess many of the key skills and experiences required for this role."
    elif match_score > 60:
        level = "good"
        detail = "Your resume shows a strong match with the job description. Most of the essential skills and experiences are present. Consider minor adjustments for an even better fit."
    elif match_score > 40:
        level = "fair"
        detail = "There's a fair match between your resume and the job description. You have some relevant skills, but there's room to improve alignment by tailoring your resume more closely to the job requirements."
    else:
        level = "low"
        detail = "The match between your resume and the job description is low. You may need to significantly revise your resume to highlight more relevant skills and experiences for this specific role."

    return (
        f"The resume matches the job description with a {level} score of {match_score}%. "
        f"{detail} "
        "Review the matched keywords and ATS-optimized resume to understand areas of strength and potential improvement."
    )

async def extract_keywords_ai(jd_text, max_keywords=20):
    """
    Uses Google Gemini 2.0 Flash to extract a list of relevant skills/keywords from a Job Description.
    Returns up to `max_keywords` as a list of strings, all in lowercase.
    """
    prompt = f"""
    Extract the top {max_keywords} technical and soft skills required from the following job description.
    Return them as a comma-separated list only. Ensure each keyword is concise and in lowercase.

    Job Description:
    {jd_text}
    """
    keyword_string = await call_gemini_api(prompt, temperature=0.2, max_tokens=150)
    if keyword_string:
        keywords = [kw.strip().lower() for kw in keyword_string.split(",") if kw.strip()]
        return keywords[:max_keywords]
    return ["Error: Could not extract keywords."]