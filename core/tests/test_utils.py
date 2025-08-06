import pytest

from core.utils import (
    compute_match_score,
    extract_skills,
    generate_ats_resume,
    generate_interview_questions,
)

@pytest.fixture
def mock_nlp(mocker):
    mock_doc = mocker.Mock()
    mock_doc.ents = [
        mocker.Mock(text="Python", label_="PRODUCT"),
        mocker.Mock(text="Django", label_="ORG"),
    ]
    mock_doc.noun_chunks = [
        mocker.Mock(text="machine learning"),
        mocker.Mock(text="data analysis"),
    ]
    mock_nlp = mocker.Mock(return_value=mock_doc)
    mocker.patch("core.utils.nlp", mock_nlp)
    return mock_nlp

def test_high_similarity_match_score(mocker):
    mock_vectorizer = mocker.patch("core.utils.TfidfVectorizer")
    mock_vectorizer_instance = mock_vectorizer.return_value
    mock_vectorizer_instance.fit_transform.return_value = [[0.5, 0.5], [0.5, 0.5]]
    mock_cosine = mocker.patch("core.utils.cosine_similarity")
    mock_cosine.return_value = [[0.95]]
    score = compute_match_score("Python developer with Django experience", "Looking for a Python developer with Django skills")
    assert score == 95.0

def test_extract_skills_from_text(mock_nlp):
    text = "Experienced in Python and Django for machine learning and data analysis."
    skills = extract_skills(text)
    # Should include both entities and noun chunks, deduplicated
    assert set(skills) == {"Python", "Django", "machine learning", "data analysis"}

def test_generate_ats_resume_appends_missing_skills(mocker):
    # Mock extract_skills to control output
    mocker.patch("core.utils.extract_skills", side_effect=[
        ["Python", "Django"],  # JD skills
    ])
    resume_text = "Experienced in Python."
    jd_text = "Looking for Python and Django skills."
    enhanced = generate_ats_resume(resume_text, jd_text)
    assert "- Django (from JD)" in enhanced
    assert enhanced.startswith(resume_text)

def test_match_score_with_empty_inputs(mocker):
    mock_vectorizer = mocker.patch("core.utils.TfidfVectorizer")
    mock_vectorizer_instance = mock_vectorizer.return_value
    # Simulate empty TF-IDF vectors
    mock_vectorizer_instance.fit_transform.return_value = [[0.0], [0.0]]
    mock_cosine = mocker.patch("core.utils.cosine_similarity")
    mock_cosine.return_value = [[0.0]]
    score = compute_match_score("", "")
    assert score == 0.0

def test_extract_skills_with_no_skills(mocker):
    mock_doc = mocker.Mock()
    mock_doc.ents = []
    mock_doc.noun_chunks = []
    mock_nlp = mocker.Mock(return_value=mock_doc)
    mocker.patch("core.utils.nlp", mock_nlp)
    skills = extract_skills("1234567890 !@#$%^&*()")
    assert skills == []

def test_generate_interview_questions_limit(mocker):
    # Mock extract_skills to return more skills than num_questions
    mocker.patch("core.utils.extract_skills", return_value=[
        "Python", "Django", "Flask", "Machine Learning", "Data Analysis", "APIs", "SQL", "Docker"
    ])
    questions = generate_interview_questions("resume", "jd", num_questions=5)
    assert len(questions) == 5
    for skill, question in zip(
        ["Python", "Django", "Flask", "Machine Learning", "Data Analysis"], questions
    ):
        assert skill in question

`Source: core/utils.py`