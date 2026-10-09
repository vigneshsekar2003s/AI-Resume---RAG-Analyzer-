def compare_resume_versions(
    before_result,
    after_result
):
    """
    Compare two resume analysis results.
    """

    # ==================================================
    # RESUME SCORE
    # ==================================================

    before_score = before_result.get(
        "score_result", {}
    ).get(
        "total_score",
        0
    )

    after_score = after_result.get(
        "score_result", {}
    ).get(
        "total_score",
        0
    )

    score_change = after_score - before_score

    # ==================================================
    # JD MATCH SCORE
    # ==================================================

    before_match = before_result.get(
        "match_result", {}
    ).get(
        "match_score",
        0
    )

    after_match = after_result.get(
        "match_result", {}
    ).get(
        "match_score",
        0
    )

    jd_match_change = after_match - before_match

    # ==================================================
    # MATCHED SKILLS
    # ==================================================

    before_skills = set(
        before_result.get(
            "match_result",
            {}
        ).get(
            "matched_skills",
            []
        )
    )

    after_skills = set(
        after_result.get(
            "match_result",
            {}
        ).get(
            "matched_skills",
            []
        )
    )

    added_skills = sorted(
        after_skills - before_skills
    )

    removed_skills = sorted(
        before_skills - after_skills
    )

    # ==================================================
    # WEAK PHRASES
    # ==================================================

    before_weak_phrases = set(
        before_result.get(
            "weak_phrases",
            []
        )
    )

    after_weak_phrases = set(
        after_result.get(
            "weak_phrases",
            []
        )
    )

    removed_weak_phrases = sorted(
        before_weak_phrases - after_weak_phrases
    )

    remaining_weak_phrases = sorted(
        after_weak_phrases
    )

    # ==================================================
    # METRICS
    # ==================================================

    before_metrics = before_result.get(
        "metrics",
        []
    )

    after_metrics = after_result.get(
        "metrics",
        []
    )

    metrics_change = (
        len(after_metrics) -
        len(before_metrics)
    )

    # ==================================================
    # RETURN COMPARISON
    # ==================================================

    return {
        "before_score": before_score,
        "after_score": after_score,
        "score_change": round(
            score_change,
            2
        ),

        "before_jd_match": before_match,
        "after_jd_match": after_match,
        "jd_match_change": round(
            jd_match_change,
            2
        ),

        "added_skills": added_skills,
        "removed_skills": removed_skills,

        "weak_phrases_before": sorted(
            before_weak_phrases
        ),

        "weak_phrases_after": sorted(
            after_weak_phrases
        ),

        "removed_weak_phrases": removed_weak_phrases,

        "remaining_weak_phrases": remaining_weak_phrases,

        "metrics_before": len(
            before_metrics
        ),

        "metrics_after": len(
            after_metrics
        ),

        "metrics_change": metrics_change
    }