import streamlit as st

from services.embedding_service import generate_embeddings
from services.vector_store import search_faiss
from services.llm_service import generate_rag_answer

from services.scoring_engine import calculate_resume_score
from services.improvement_service import generate_resume_improvements
from services.resume_pipeline import analyze_resume
from services.jd_matcher import match_resume_with_jd
from services.comparison_service import compare_resume_versions

# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="🤖",
    layout="wide"
)


# ==================================================
# TITLE
# ==================================================

st.title(
    "🤖 AI Resume Analyzer"
)

st.write(
    "Upload your resume PDF to extract, analyze, and ask "
    "questions about your resume using AI."
)


# ==================================================
# RESUME UPLOAD
# ==================================================

uploaded_file = st.file_uploader(
    "Upload your Resume",
    type=["pdf"]
)


# ==================================================
# PROCESS RESUME
# ==================================================

if uploaded_file:

    # ==================================================
    # RUN COMPLETE RESUME PIPELINE
    # ==================================================

    analysis_result = analyze_resume(
    uploaded_file
)


    # ==================================================
    # GET PIPELINE RESULTS
    # ==================================================

    resume_text = analysis_result["resume_text"]

    cleaned_text = analysis_result["cleaned_text"]

    sections = analysis_result["sections"]

    chunks = analysis_result["chunks"]

    embeddings = analysis_result["embeddings"]

    faiss_index = analysis_result["faiss_index"]

    buzzwords = analysis_result["buzzwords"]

    action_verbs = analysis_result["action_verbs"]

    weak_phrases = analysis_result["weak_phrases"]

    repeated_words = analysis_result["repeated_words"]

    metrics = analysis_result["metrics"]


    # ==================================================
    # SUCCESS MESSAGE
    # ==================================================

    st.success(
        "Resume uploaded and processed successfully!"
    )


    # ==================================================
    # RESUME INTELLIGENCE
    # ==================================================

    st.subheader(
        "📊 Resume Intelligence"
    )


    # ==================================================
    # BUZZWORDS
    # ==================================================

    st.write(
        "### 🔑 Buzzwords"
    )

    if buzzwords:

        st.warning(
            f"Found {len(buzzwords)} common resume buzzwords."
        )

        st.write(
            ", ".join(buzzwords)
        )

    else:

        st.success(
            "No common resume buzzwords detected."
        )


    # ==================================================
    # ACTION VERBS
    # ==================================================

    st.write(
        "### 💪 Action Verbs"
    )

    if action_verbs:

        st.success(
            f"Found {len(action_verbs)} strong action verbs."
        )

        st.write(
            ", ".join(action_verbs)
        )

    else:

        st.warning(
            "Few strong action verbs were detected."
        )


    # ==================================================
    # WEAK PHRASES
    # ==================================================

    st.write(
        "### ⚠️ Weak Phrases"
    )

    if weak_phrases:

        st.warning(
            f"Found {len(weak_phrases)} weak resume phrases."
        )

        st.write(
            ", ".join(weak_phrases)
        )

    else:

        st.success(
            "No common weak phrases detected."
        )


    # ==================================================
    # REPEATED WORDS
    # ==================================================

    st.write(
        "### 🔁 Repeated Words"
    )

    if repeated_words:

        for word, count in repeated_words.items():

            st.write(
                f"**{word}** → {count} times"
            )

    else:

        st.success(
            "No highly repeated words detected."
        )


    # ==================================================
    # METRICS
    # ==================================================

    st.write(
        "### 📈 Metrics & Achievements"
    )

    if metrics:

        st.success(
            f"Detected {len(metrics)} measurable values."
        )

        st.write(
            ", ".join(metrics)
        )

    else:

        st.warning(
            "No measurable metrics detected."
        )


    # ==================================================
    # JOB DESCRIPTION MATCHING
    # ==================================================

    st.subheader(
        "🎯 Job Description Matching"
    )

    st.write(
        "Paste a job description to compare its technical "
        "requirements with your resume."
    )


    job_description = st.text_area(
        "Job Description",
        placeholder=(
            "Paste the job description here...\n\n"
            "Example:\n"
            "We are looking for a Python developer with "
            "experience in FastAPI, PostgreSQL, Docker, "
            "REST APIs and React."
        ),
        height=250
    )


    # ==================================================
    # JOB DESCRIPTION ANALYSIS
    # ==================================================

    

    # ==================================================
    # MATCH RESUME WITH JD
    # ==================================================

    match_result = match_resume_with_jd(
        cleaned_text,
        job_description
    )

    if job_description.strip():

        match_score = match_result["match_score"]

        matched_skills = match_result["matched_skills"]

        missing_skills = match_result["missing_skills"]

        jd_skills = match_result["jd_skills"]


        # ==================================================
        # JOB MATCH SCORE
        # ==================================================

        st.write(
            "### 📊 Job Match Score"
        )

        st.metric(
            label="JD Match",
            value=f"{match_score}%"
        )

        st.progress(
            int(match_score)
        )


        # ==================================================
        # JD SKILLS
        # ==================================================

        st.write(
            "### 🔎 Skills Found in Job Description"
        )

        if jd_skills:

            st.write(
                ", ".join(jd_skills)
            )

        else:

            st.warning(
                "No recognized technical skills were found "
                "in the job description."
            )


        # ==================================================
        # MATCHED SKILLS
        # ==================================================

        st.write(
            "### ✅ Matched Skills"
        )

        if matched_skills:

            for skill in matched_skills:

                st.write(
                    f"✅ {skill}"
                )

        else:

            st.warning(
                "No matching technical skills were found."
            )


        # ==================================================
        # MISSING SKILLS
        # ==================================================

        st.write(
            "### ⚠️ Missing Skills"
        )

        if missing_skills:

            for skill in missing_skills:

                st.write(
                    f"⚠️ {skill}"
                )

            st.info(
                "Only add missing skills to your resume if "
                "you genuinely have relevant knowledge or experience."
            )

        else:

            st.success(
                "No recognized technical skills are missing."
            )


        # ==================================================
        # RESUME OPTIMIZATION SCORE
        # ==================================================

        score_result = calculate_resume_score(
            jd_match_score=match_score,
            matched_skills=matched_skills,
            action_verbs=action_verbs,
            buzzwords=buzzwords,
            repeated_words=repeated_words,
            metrics=metrics,
            sections=sections,
            weak_phrases=weak_phrases
        )


        # ==================================================
        # DISPLAY SCORE
        # ==================================================

        st.subheader(
            "🏆 Resume Optimization Score"
        )

        score = score_result["total_score"]

        label = score_result["label"]


        st.metric(
            "Overall Score",
            f"{score}/100"
        )


        st.progress(
            score
        )


        st.write(
            f"### {label}"
        )


        # ==================================================
        # SCORE BREAKDOWN
        # ==================================================

        st.write(
            "### 📊 Score Breakdown"
        )


        col1, col2, col3, col4 = st.columns(4)


        with col1:

            st.metric(
                "🎯 JD Match",
                f"{score_result['jd_score']}/25"
            )


        with col2:

            st.metric(
                "🔑 Keywords",
                f"{score_result['keyword_score']}/20"
            )


        with col3:

            st.metric(
                "💻 Technical Skills",
                f"{score_result['technical_score']}/15"
            )


        with col4:

            st.metric(
                "💪 Action Verbs",
                f"{score_result['action_score']}/10"
            )


        col5, col6, col7, col8 = st.columns(4)


        with col5:

            st.metric(
                "🔁 Repetition",
                f"{score_result['repetition_score']}/10"
            )


        with col6:

            st.metric(
                "📑 Structure",
                f"{score_result['structure_score']}/10"
            )


        with col7:

            st.metric(
                "📈 Metrics",
                f"{score_result['metrics_score']}/5"
            )


        with col8:

            st.metric(
                "🤖 ATS",
                f"{score_result['ats_score']}/5"
            )


        # ==================================================
        # AI IMPROVEMENT RECOMMENDATIONS
        # ==================================================

        st.subheader(
            "🤖 AI Improvement Recommendations"
        )

        st.write(
            "Get AI-powered recommendations based on "
            "your resume analysis and job description."
        )


        generate_improvements = st.button(
            "✨ Generate AI Recommendations"
        )


        if generate_improvements:

            with st.spinner(
                "Analyzing your resume and generating recommendations..."
            ):

                try:

                    recommendations = generate_resume_improvements(
                        resume_text=cleaned_text,
                        score_result=score_result,
                        missing_skills=missing_skills,
                        buzzwords=buzzwords,
                        repeated_words=repeated_words,
                        weak_phrases=weak_phrases,
                        metrics=metrics,
                        sections=sections
                    )


                    st.write(
                        "### 💡 AI Recommendations"
                    )


                    st.markdown(
                        recommendations
                    )


                except Exception as e:

                    st.error(
                        f"Error generating recommendations: {e}"
                    )

# ==================================================
# BEFORE VS AFTER RESUME COMPARISON
# ==================================================

st.divider()

st.header(
    "📊 Before vs After Resume Comparison"
)

st.write(
    "Upload your original resume and improved resume "
    "to compare your resume optimization progress."
)


# ==================================================
# JOB DESCRIPTION
# ==================================================

comparison_jd = st.text_area(
    "📋 Job Description for Comparison",
    height=180,
    placeholder=(
        "Paste the same Job Description used "
        "for both resume versions..."
    ),
    key="comparison_jd"
)


# ==================================================
# RESUME UPLOADS
# ==================================================

before_file = st.file_uploader(
    "Upload Original Resume",
    type=["pdf"],
    key="before_resume"
)

after_file = st.file_uploader(
    "Upload Improved Resume",
    type=["pdf"],
    key="after_resume"
)


# ==================================================
# COMPARE RESUMES
# ==================================================

if (
    before_file
    and after_file
    and comparison_jd.strip()
):

    if st.button(
        "🔍 Compare Resumes",
        use_container_width=True
    ):

        with st.spinner(
            "Analyzing both resume versions..."
        ):

            # ==========================================
            # ORIGINAL RESUME
            # ==========================================

            before_result = analyze_resume(
                before_file
            )


            # ==========================================
            # IMPROVED RESUME
            # ==========================================

            after_result = analyze_resume(
                after_file
            )


            # ==========================================
            # JD MATCH - ORIGINAL
            # ==========================================

            before_match = match_resume_with_jd(
                before_result["cleaned_text"],
                comparison_jd
            )

            before_result["match_result"] = (
                before_match
            )


            # ==========================================
            # JD MATCH - IMPROVED
            # ==========================================

            after_match = match_resume_with_jd(
                after_result["cleaned_text"],
                comparison_jd
            )

            after_result["match_result"] = (
                after_match
            )


            # ==========================================
            # SCORE - ORIGINAL
            # ==========================================

            before_result["score_result"] = (
                calculate_resume_score(
                    jd_match_score=before_match[
                        "match_score"
                    ],
                    matched_skills=before_match[
                        "matched_skills"
                    ],
                    action_verbs=before_result[
                        "action_verbs"
                    ],
                    buzzwords=before_result[
                        "buzzwords"
                    ],
                    repeated_words=before_result[
                        "repeated_words"
                    ],
                    metrics=before_result[
                        "metrics"
                    ],
                    sections=before_result[
                        "sections"
                    ],
                    weak_phrases=before_result[
                        "weak_phrases"
                    ]
                )
            )


            # ==========================================
            # SCORE - IMPROVED
            # ==========================================

            after_result["score_result"] = (
                calculate_resume_score(
                    jd_match_score=after_match[
                        "match_score"
                    ],
                    matched_skills=after_match[
                        "matched_skills"
                    ],
                    action_verbs=after_result[
                        "action_verbs"
                    ],
                    buzzwords=after_result[
                        "buzzwords"
                    ],
                    repeated_words=after_result[
                        "repeated_words"
                    ],
                    metrics=after_result[
                        "metrics"
                    ],
                    sections=after_result[
                        "sections"
                    ],
                    weak_phrases=after_result[
                        "weak_phrases"
                    ]
                )
            )


            # ==========================================
            # COMPARE BOTH
            # ==========================================

            comparison = compare_resume_versions(
                before_result,
                after_result
            )


        # ==================================================
        # SCORE COMPARISON
        # ==================================================

        st.subheader(
            "📈 Score Comparison"
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Before Score",
                before_result[
                    "score_result"
                ]["total_score"]
            )

        with col2:

            st.metric(
                "After Score",
                after_result[
                    "score_result"
                ]["total_score"]
            )

        with col3:

            st.metric(
                "Improvement",
                f"{comparison['score_change']:+.2f}"
            )


        # ==================================================
        # JD MATCH COMPARISON
        # ==================================================

        st.subheader(
            "🎯 JD Match Comparison"
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Before JD Match",
                f"{comparison['before_jd_match']:.2f}%"
            )

        with col2:

            st.metric(
                "After JD Match",
                f"{comparison['after_jd_match']:.2f}%"
            )

        with col3:

            st.metric(
                "JD Match Improvement",
                f"{comparison['jd_match_change']:+.2f}%"
            )


        # ==================================================
        # SKILL CHANGES
        # ==================================================

        st.subheader(
            "🛠️ Skill Changes"
        )

        col1, col2 = st.columns(2)

        with col1:

            st.markdown(
                "### ✅ Skills Added"
            )

            if comparison["added_skills"]:

                for skill in comparison[
                    "added_skills"
                ]:

                    st.success(
                        skill
                    )

            else:

                st.info(
                    "No new matched skills detected."
                )

        with col2:

            st.markdown(
                "### ➖ Skills Removed"
            )

            if comparison["removed_skills"]:

                for skill in comparison[
                    "removed_skills"
                ]:

                    st.warning(
                        skill
                    )

            else:

                st.info(
                    "No matched skills were removed."
                )


        # ==================================================
        # WRITING IMPROVEMENTS
        # ==================================================

        st.subheader(
            "✍️ Writing Improvements"
        )

        col1, col2 = st.columns(2)

        with col1:

            st.markdown(
                "### ✅ Weak Phrases Removed"
            )

            if comparison[
                "removed_weak_phrases"
            ]:

                for phrase in comparison[
                    "removed_weak_phrases"
                ]:

                    st.success(
                        phrase
                    )

            else:

                st.info(
                    "No weak phrases were removed."
                )

        with col2:

            st.markdown(
                "### ⚠️ Remaining Weak Phrases"
            )

            if comparison[
                "remaining_weak_phrases"
            ]:

                for phrase in comparison[
                    "remaining_weak_phrases"
                ]:

                    st.warning(
                        phrase
                    )

            else:

                st.success(
                    "No weak phrases detected."
                )


        # ==================================================
        # ACHIEVEMENT METRICS
        # ==================================================

        st.subheader(
            "📊 Achievement Metrics"
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Before",
                comparison["metrics_before"]
            )

        with col2:

            st.metric(
                "After",
                comparison["metrics_after"]
            )

        with col3:

            change = comparison[
                "metrics_change"
            ]

            st.metric(
                "Change",
                f"{change:+d}"
            )