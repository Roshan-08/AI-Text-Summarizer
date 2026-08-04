from google import genai

from app.config.settings import GEMINI_API_KEY, MODEL_NAME
from app.prompts.summary_prompt import SUMMARY_PROMPT

class SummaryService:

    def __init__(self):
        self.client = genai.Client(api_key=GEMINI_API_KEY)

    def generate_summary(self, text, style):
        prompt = SUMMARY_PROMPT[style].format(text=text)

        response = self.client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        return response.text