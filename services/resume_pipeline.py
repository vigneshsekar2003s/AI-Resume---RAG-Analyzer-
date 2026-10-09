from services.pdf_processor import extract_text_from_pdf
from services.text_processor import clean_text, detect_sections
from services.chunker import create_chunks
from services.embedding_service import generate_embeddings
from services.vector_store import create_faiss_index

from services.resume_analyzer import (
    detect_buzzwords,
    detect_action_verbs,
    detect_weak_phrases,
    detect_repeated_words,
    detect_metrics
)

from services.jd_matcher import match_resume_with_jd
from services.scoring_engine import calculate_resume_score


def analyze_resume(uploaded_file, job_description=""):
    # ---------------------------------
    # 1. Extract resume text
    # ---------------------------------
    resume_text = extract_text_from_pdf(uploaded_file)

    # ---------------------------------
    # 2. Clean resume text
    # ---------------------------------
    cleaned_text = clean_text(resume_text)

    # ---------------------------------
    # 3. Detect resume sections
    # ---------------------------------
    sections = detect_sections(cleaned_text)

    # ---------------------------------
    # 4. Create text chunks
    # ---------------------------------
    chunks = create_chunks(cleaned_text)

    # ---------------------------------
    # 5. Generate embeddings
    # ---------------------------------
    embeddings = generate_embeddings(chunks)

    # ---------------------------------
    # 6. Create FAISS index
    # ---------------------------------
    faiss_index = create_faiss_index(embeddings)

    # ---------------------------------
    # 7. Resume intelligence analysis
    # ---------------------------------
    buzzwords = detect_buzzwords(cleaned_text)
    action_verbs = detect_action_verbs(cleaned_text)
    weak_phrases = detect_weak_phrases(cleaned_text)
    repeated_words = detect_repeated_words(cleaned_text)
    metrics = detect_metrics(cleaned_text)

    # ---------------------------------
    # 8. Default JD result
    # ---------------------------------
    match_result = {
        "resume_skills": [],
        "jd_skills": [],
        "matched_skills": [],
        "missing_skills": [],
        "match_score": 0
    }

    score_result = None

    # ---------------------------------
    # 9. JD matching + scoring
    # ---------------------------------
    if job_description.strip():

        match_result = match_resume_with_jd(
            cleaned_text,
            job_description
        )

        score_result = calculate_resume_score(
            jd_match_score=match_result["match_score"],
            matched_skills=match_result["matched_skills"],
            action_verbs=action_verbs,
            buzzwords=buzzwords,
            repeated_words=repeated_words,
            metrics=metrics,
            sections=sections,
            weak_phrases=weak_phrases
        )

    # ---------------------------------
    # 10. Return complete analysis
    # ---------------------------------
    return {
        "resume_text": resume_text,
        "cleaned_text": cleaned_text,
        "sections": sections,
        "chunks": chunks,
        "embeddings": embeddings,
        "faiss_index": faiss_index,

        "buzzwords": buzzwords,
        "action_verbs": action_verbs,
        "weak_phrases": weak_phrases,
        "repeated_words": repeated_words,
        "metrics": metrics,

        "match_result": match_result,
        "score_result": score_result
    }