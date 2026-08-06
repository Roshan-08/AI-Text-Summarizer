import time
from google import genai
import logging

logger = logging.getLogger(__name__)

from app.prompts.summary_prompt import SUMMARY_PROMPT
from app.config.settings import (
    GEMINI_API_KEY,
    MODEL_NAME,
    CACHE_TTL,
)

class SummaryService:

    def __init__(self):
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.cache = {}
        self.cache_ttl = CACHE_TTL

    def generate_summary(self, text, style):

        cache_key = f"{text}:{style}"

        if cache_key in self.cache:

            cache_item = self.cache[cache_key]

            age = time.time() - cache_item["created_at"]

            if age < self.cache_ttl:
                logger.info(f"Cache HIT: {cache_key}")
                return cache_item["summary"]

            logger.info(f"Cache EXPIRED: {cache_key}")
            del self.cache[cache_key]

        logger.info(f"Cache MISS: {cache_key}")

        prompt = SUMMARY_PROMPT[style].format(text=text)

        response = self.client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        summary = response.text

        self.cache[cache_key] = {
            "summary": summary,
            "created_at": time.time()
}

        return summary