import os

from groq import Groq
from dotenv import load_dotenv


load_dotenv()


client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def generate_resume_improvements(
    resume_text,
    score_result,
    missing_skills,
    buzzwords,
    repeated_words,
    weak_phrases,
    metrics,
    sections
):
    """
    Generate AI-powered resume improvement recommendations.
    """

    prompt = f"""
You are an AI Resume Optimization Assistant.

Analyze the resume information provided below and give
practical recommendations to improve the resume.

IMPORTANT RULES:

1. Do NOT invent skills.
2. Do NOT invent experience.
3. Do NOT invent projects.
4. Do NOT invent achievements.
5. Do NOT invent numbers or metrics.
6. Do NOT recommend adding a skill unless the candidate
   genuinely has that skill.
7. Base recommendations only on the provided information.
8. Keep recommendations concise and actionable.
9. Focus on improving resume quality for job applications.
10. Do not claim that the score guarantees ATS selection.

--------------------------------------------------
RESUME OPTIMIZATION SCORE
--------------------------------------------------

Overall Score:
{score_result["total_score"]}/100

Score Label:
{score_result["label"]}

JD Match:
{score_result["jd_score"]}/25

Keywords:
{score_result["keyword_score"]}/20

Technical Skills:
{score_result["technical_score"]}/15

Action Verbs:
{score_result["action_score"]}/10

Repetition:
{score_result["repetition_score"]}/10

Structure:
{score_result["structure_score"]}/10

Metrics:
{score_result["metrics_score"]}/5

ATS:
{score_result["ats_score"]}/5


--------------------------------------------------
MISSING JOB DESCRIPTION SKILLS
--------------------------------------------------

{missing_skills}


--------------------------------------------------
RESUME BUZZWORDS
--------------------------------------------------

{buzzwords}


--------------------------------------------------
REPEATED WORDS
--------------------------------------------------

{repeated_words}


--------------------------------------------------
WEAK PHRASES
--------------------------------------------------

{weak_phrases}


--------------------------------------------------
RESUME METRICS
--------------------------------------------------

{metrics}


--------------------------------------------------
RESUME SECTIONS
--------------------------------------------------

{sections}


--------------------------------------------------
RESUME TEXT
--------------------------------------------------

{resume_text}


--------------------------------------------------
OUTPUT FORMAT
--------------------------------------------------

Provide recommendations using these sections:

### 🔥 Top 3 Improvements

Give the three most important improvements.

### 🎯 Job Description Improvements

Explain how the resume can better match the job description.

### ✍️ Writing Improvements

Identify weak phrases, buzzwords, repeated wording,
or weak action verbs.

### 📊 Achievement Improvements

Explain where measurable achievements could be added
ONLY when the resume genuinely contains measurable
information.

### 📑 Structure Improvements

Suggest improvements to resume organization and sections.

### 💡 Final Recommendation

Give a short overall recommendation.

Do not rewrite the entire resume.
Focus on actionable improvements.
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    return response.choices[0].message.content