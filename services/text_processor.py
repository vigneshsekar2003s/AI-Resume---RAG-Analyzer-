import re


def clean_text(text):
    """
    Clean extracted resume text while preserving useful information.
    """

    # Normalize line endings
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    # Remove excessive spaces/tabs
    text = re.sub(r"[ \t]+", " ", text)

    # Remove excessive blank lines
    text = re.sub(r"\n\s*\n+", "\n\n", text)

    # Remove leading/trailing spaces from each line
    lines = [line.strip() for line in text.splitlines()]

    # Remove completely empty lines
    lines = [line for line in lines if line]

    return "\n".join(lines).strip()


def detect_sections(text):
    """
    Detect common resume sections.
    """

    section_patterns = {
        "summary": [
            "professional summary",
            "summary",
            "profile",
            "objective"
        ],
        "skills": [
            "technical skills",
            "skills",
            "technical expertise"
        ],
        "experience": [
            "professional experience",
            "work experience",
            "experience",
            "internship",
            "internships"
        ],
        "projects": [
            "projects",
            "personal projects",
            "academic projects"
        ],
        "education": [
            "education",
            "academic background"
        ],
        "certifications": [
            "certifications",
            "certificates",
            "courses"
        ]
    }

    detected = {}

    lines = text.splitlines()

    for line in lines:
        normalized_line = line.lower().strip()

        for section_name, patterns in section_patterns.items():

            if normalized_line in patterns:
                detected[section_name] = line.strip()

    return detected