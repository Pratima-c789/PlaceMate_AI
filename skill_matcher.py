import re

SKILL_DATABASE = {
    "Programming Languages": [
        "C", "C++", "Java", "Python",
        "SQL", "JavaScript", "C#"
    ],

    "AI and Machine Learning": [
        "Artificial Intelligence",
        "Machine Learning",
        "Deep Learning",
        "NLP",
        "Pandas",
        "NumPy",
        "Scikit-learn",
        "TensorFlow",
        "PyTorch",
        "Random Forest"
    ],

    "Web Development": [
        "HTML", "CSS", "React.js",
        "Node.js", "Flask", "Django",
        "Streamlit", "Spring Boot"
    ],

    "Databases": [
        "MySQL", "MongoDB", "SQLite",
        "PostgreSQL", "DBMS"
    ],

    "Tools and Platforms": [
        "Git", "GitHub", "Docker",
        "AWS", "Linux", "Jenkins",
        "VS Code", "Kubernetes"
    ],

    "Core Computer Science": [
        "Data Structures",
        "Algorithms",
        "OOP",
        "Operating Systems",
        "Computer Networks"
    ]
}


def extract_skills(text):

    detected_skills = {}

    for category, skills in SKILL_DATABASE.items():

        matched = []

        for skill in skills:

            pattern = (
                r"(?<![\w+#])"
                + re.escape(skill)
                + r"(?![\w+#])"
            )

            if re.search(pattern, text, re.IGNORECASE):
                matched.append(skill)

        if matched:
            detected_skills[category] = matched

    return detected_skills
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def calculate_similarity(resume_text, job_description):

    if not resume_text.strip() or not job_description.strip():
        return 0.0

    vectorizer = TfidfVectorizer(
        stop_words="english"
    )

    try:
        vectors = vectorizer.fit_transform(
            [resume_text, job_description]
        )
    except ValueError:
        return 0.0

    similarity = cosine_similarity(
        vectors[0:1],
        vectors[1:2]
    )[0][0]

    return round(float(similarity) * 100, 2)


def compare_skills(resume_text, job_description):

    resume_categories = extract_skills(resume_text)
    job_categories = extract_skills(job_description)

    resume_skills = {
        skill
        for skills in resume_categories.values()
        for skill in skills
    }

    job_skills = {
        skill
        for skills in job_categories.values()
        for skill in skills
    }

    matched = resume_skills & job_skills
    missing = job_skills - resume_skills

    coverage = (
        round(len(matched) / len(job_skills) * 100, 2)
        if job_skills else None
    )

    return {
        "matched": sorted(matched),
        "missing": sorted(missing),
        "coverage": coverage
    }
PREPARATION_DATABASE = {
    "Quantitative Aptitude": [
        "quantitative aptitude",
        "numerical ability",
        "arithmetic"
    ],

    "Logical Reasoning": [
        "logical reasoning",
        "analytical ability",
        "logical ability"
    ],

    "English and Verbal Ability": [
        "english",
        "verbal ability",
        "communication skills"
    ],

    "Programming and Coding": [
        "programming",
        "coding",
        "coding test"
    ],

    "Computer Science Fundamentals": [
        "computer science fundamentals",
        "computer science & engineering fundamentals",
        "computer science and engineering fundamentals",
        "cs fundamentals"
    ],

    "Technical Interview": [
        "technical interview",
        "technical face-to-face"
    ],

    "HR Interview": [
        "hr interview",
        "hr round"
    ]
}


def extract_preparation_areas(job_description):

    detected_areas = []

    text = job_description.lower()

    for area, keywords in PREPARATION_DATABASE.items():

        if any(keyword in text for keyword in keywords):

            detected_areas.append(area)

    return detected_areas