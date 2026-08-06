from fastapi import HTTPException


def validate_text(text: str):

    cleaned_text = text.strip()

    if len(cleaned_text.split()) < 10:
        raise HTTPException(
            status_code=400,
            detail="Text is too short for summarization."
        )

    return cleaned_text