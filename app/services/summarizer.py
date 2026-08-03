from google import genai

from app.config.settings import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)


def generate_summary(text):
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=f"Summarize the following text in 2-3 sentences:\n\n{text}",
    )

    return response.text