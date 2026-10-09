import re


# --------------------------------------------------
# COMMON TECHNICAL SKILLS
# --------------------------------------------------

TECHNICAL_SKILLS = [
    "python",
    "java",
    "javascript",
    "typescript",
    "c",
    "c++",
    "c#",
    "react",
    "react.js",
    "node.js",
    "node",
    "express",
    "express.js",
    "mongodb",
    "mysql",
    "postgresql",
    "sql",
    "html",
    "css",
    "tailwind",
    "tailwind css",
    "git",
    "github",
    "docker",
    "kubernetes",
    "aws",
    "azure",
    "fastapi",
    "flask",
    "django",
    "rest api",
    "rest apis",
    "api",
    "apis",
    "jwt",
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "ai",
    "rag",
    "faiss",
    "streamlit",
    "openai",
    "groq",
    "langchain",
    "tensorflow",
    "pytorch",
    "pandas",
    "numpy"
]


# --------------------------------------------------
# EXTRACT TECHNICAL SKILLS
# --------------------------------------------------

def extract_skills(text):
    """
    Extract known technical skills from text.
    """

    text_lower = text.lower()

    found_skills = []

    for skill in TECHNICAL_SKILLS:

        pattern = rf"(?<!\w){re.escape(skill.lower())}(?!\w)"

        if re.search(pattern, text_lower):

            found_skills.append(skill)

    return sorted(
        set(found_skills)
    )


# --------------------------------------------------
# COMPARE RESUME WITH JD
# --------------------------------------------------

def match_resume_with_jd(
    resume_text,
    job_description
):
    """
    Compare resume skills with job description skills.
    """

    resume_skills = extract_skills(
        resume_text
    )

    jd_skills = extract_skills(
        job_description
    )

    matched_skills = [
        skill
        for skill in jd_skills
        if skill in resume_skills
    ]

    missing_skills = [
        skill
        for skill in jd_skills
        if skill not in resume_skills
    ]

    if jd_skills:

        match_score = (
            len(matched_skills)
            / len(jd_skills)
        ) * 100

    else:

        match_score = 0

    return {
        "resume_skills": resume_skills,
        "jd_skills": jd_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "match_score": round(
            match_score,
            2
        )
    }