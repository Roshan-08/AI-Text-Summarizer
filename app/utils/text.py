import re


def clean_text(text: str) -> str:
    """
    Clean user input before sending it to the AI model.
    """

    text = text.strip()

    text = re.sub(r"\s+", " ", text)

    return text