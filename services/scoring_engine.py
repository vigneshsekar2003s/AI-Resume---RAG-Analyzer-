# --------------------------------------------------
# RESUME OPTIMIZATION SCORING ENGINE
# --------------------------------------------------


def calculate_resume_score(
    jd_match_score,
    matched_skills,
    action_verbs,
    buzzwords,
    repeated_words,
    metrics,
    sections,
    weak_phrases
):
    """
    Calculate a transparent 100-point
    Resume Optimization Score.

    Score Breakdown:
    - JD Match              25 points
    - Keyword Optimization 15 points
    - Technical Skills      15 points
    - Action Verbs          10 points
    - Repetition            10 points
    - Resume Structure      10 points
    - Metrics                5 points
    - ATS Readiness          10 points
    ------------------------------------------------
    Total                  100 points
    """

    # --------------------------------------------------
    # 1. JOB DESCRIPTION MATCH — 25 POINTS
    # --------------------------------------------------

    jd_score = jd_match_score * 0.25

    # --------------------------------------------------
    # 2. KEYWORD OPTIMIZATION — 15 POINTS
    # --------------------------------------------------
    #
    # Measures keyword coverage from the matched skills.
    # Capped at 15 points.
    #

    keyword_score = min(
        len(matched_skills) * 1.5,
        15
    )

    # --------------------------------------------------
    # 3. TECHNICAL SKILLS — 15 POINTS
    # --------------------------------------------------
    #
    # Technical skill breadth is evaluated separately
    # from the JD match score.
    #
    # We use a diminishing contribution so that having
    # many matched skills does not excessively increase
    # the final score.
    #

    technical_skill_count = len(
        matched_skills
    )

    if technical_skill_count == 0:

        technical_score = 0

    elif technical_skill_count <= 3:

        technical_score = 5

    elif technical_skill_count <= 6:

        technical_score = 9

    elif technical_skill_count <= 10:

        technical_score = 12

    else:

        technical_score = 15

    # --------------------------------------------------
    # 4. ACTION VERBS — 10 POINTS
    # --------------------------------------------------

    action_score = min(
        len(action_verbs) * 1,
        10
    )

    # --------------------------------------------------
    # 5. REPETITION — 10 POINTS
    # --------------------------------------------------

    repeated_count = len(
        repeated_words
    )

    if repeated_count == 0:

        repetition_score = 10

    elif repeated_count <= 2:

        repetition_score = 8

    elif repeated_count <= 4:

        repetition_score = 6

    elif repeated_count <= 6:

        repetition_score = 4

    else:

        repetition_score = 2

    # --------------------------------------------------
    # 6. RESUME STRUCTURE — 10 POINTS
    # --------------------------------------------------

    expected_sections = {
        "summary",
        "skills",
        "experience",
        "projects",
        "education"
    }

    detected_section_names = set(
        sections.keys()
    )

    section_ratio = (
        len(
            expected_sections
            & detected_section_names
        )
        / len(expected_sections)
    )

    structure_score = (
        section_ratio * 10
    )

    # --------------------------------------------------
    # 7. METRICS & ACHIEVEMENTS — 5 POINTS
    # --------------------------------------------------

    metrics_score = min(
        len(metrics) * 0.5,
        5
    )

    # --------------------------------------------------
    # 8. ATS READINESS — 10 POINTS
    # --------------------------------------------------
    #
    # Starts at 10 and applies deductions for:
    # - Excessive weak phrases
    # - Excessive buzzwords
    # - Poor section structure
    #

    ats_score = 10

    if len(weak_phrases) >= 3:

        ats_score -= 2

    if len(buzzwords) >= 5:

        ats_score -= 1

    if len(sections) < 3:

        ats_score -= 2

    ats_score = max(
        ats_score,
        0
    )

    # --------------------------------------------------
    # FINAL SCORE
    # --------------------------------------------------

    total_score = (
        jd_score
        + keyword_score
        + technical_score
        + action_score
        + repetition_score
        + structure_score
        + metrics_score
        + ats_score
    )

    total_score = min(
        round(total_score),
        100
    )

    # --------------------------------------------------
    # SCORE LABEL
    # --------------------------------------------------

    if total_score >= 90:

        label = "Excellent"

    elif total_score >= 80:

        label = "Strong"

    elif total_score >= 70:

        label = "Good"

    elif total_score >= 60:

        label = "Needs Improvement"

    else:

        label = "Needs Major Improvement"

    # --------------------------------------------------
    # RETURN SCORE DETAILS
    # --------------------------------------------------

    return {
        "total_score": total_score,
        "label": label,

        "jd_score": round(
            jd_score,
            2
        ),

        "keyword_score": round(
            keyword_score,
            2
        ),

        "technical_score": round(
            technical_score,
            2
        ),

        "action_score": round(
            action_score,
            2
        ),

        "repetition_score": round(
            repetition_score,
            2
        ),

        "structure_score": round(
            structure_score,
            2
        ),

        "metrics_score": round(
            metrics_score,
            2
        ),

        "ats_score": round(
            ats_score,
            2
        )
    }