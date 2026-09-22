import time
import hashlib
from google import genai
import logging

logger = logging.getLogger(__name__)

from app.prompts.summary_prompt import SUMMARY_PROMPT
from app.config.settings import settings


class SummaryService:

    def __init__(self):
        self.client = genai.Client(api_key=settings.gemini_api_key)
        self.cache = {}
        self.cache_ttl = settings.cache_ttl
        self.cache_max_size = settings.cache_max_size

    def _build_cache_key(self, text, style):
        cache_input = f"{text}:{style}"
        return hashlib.sha256(cache_input.encode("utf-8")).hexdigest()

    def generate_summary(self, text, style):

        cache_key = self._build_cache_key(text, style)

        if cache_key in self.cache:

            cache_item = self.cache[cache_key]

            age = time.time() - cache_item["created_at"]

            if age < self.cache_ttl:
                logger.info(
                    "Cache HIT | style=%s | text_length=%d",
                    style,
                    len(text)
                )
                return cache_item["summary"]

            logger.info(
                "Cache EXPIRED | style=%s | text_length=%d",
                style,
                len(text)
            )
            del self.cache[cache_key]

        logger.info(
            "Cache MISS | style=%s | text_length=%d",
            style,
            len(text)
        )

        prompt = SUMMARY_PROMPT[style].format(text=text)

        logger.info(
            "Generating summary | style=%s | model=%s",
            style,
            settings.model_name
        )

        try:
            response = self.client.models.generate_content(
                model=settings.model_name,
                contents=prompt
            )

        except Exception:
            logger.exception(
                "Gemini request failed | style=%s | text_length=%d",
                style,
                len(text)
            )
            raise

        summary = response.text

        if len(self.cache) >= self.cache_max_size:
            oldest_key = next(iter(self.cache))
            del self.cache[oldest_key]

            logger.info(
                "Cache EVICT | cache_size=%d",
                len(self.cache)
            )

        self.cache[cache_key] = {
            "summary": summary,
            "created_at": time.time()
        }

        return summary