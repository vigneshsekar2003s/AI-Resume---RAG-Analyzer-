import os

from groq import Groq
from dotenv import load_dotenv


load_dotenv()


client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def generate_rag_answer(question, context):
    """
    Generate an answer using only the retrieved resume context.
    """

    prompt = f"""
You are an AI Resume Assistant.

Answer the user's question using ONLY the resume context provided below.

Rules:
1. Do not invent information.
2. Do not add skills, projects, experience, or achievements
   that are not present in the context.
3. If the answer is not available in the context, say:
   "I couldn't find this information in the resume."
4. Keep the answer clear and concise.
5. Use bullet points when appropriate.

Resume Context:
----------------
{context}
----------------

User Question:
{question}

Answer:
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content