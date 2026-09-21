import time
import pytest
from unittest.mock import MagicMock

from app.services.summarizer import SummaryService
from app.config.settings import settings

def test_generate_summary_cache_miss():
    fake_client = MagicMock()

    fake_client.models.generate_content.return_value.text = (
        "Artificial Intelligence is transforming healthcare."
    )

    service = SummaryService.__new__(SummaryService)

    service.client = fake_client
    service.cache = {}
    service.cache_ttl = 300

    text = (
        "Artificial Intelligence is transforming healthcare "
        "by helping doctors diagnose diseases more accurately."
    )

    result = service.generate_summary(text, "short")

    assert result == "Artificial Intelligence is transforming healthcare."

    fake_client.models.generate_content.assert_called_once()

    call_args = fake_client.models.generate_content.call_args

    assert call_args.kwargs["model"] == settings.model_name
    assert text in call_args.kwargs["contents"]

    cache_key = f"{text}:short"

    assert cache_key in service.cache
    assert service.cache[cache_key]["summary"] == result

def test_generate_summary_cache_hit():
    fake_client = MagicMock()

    service = SummaryService.__new__(SummaryService)

    service.client = fake_client
    service.cache = {}
    service.cache_ttl = 300

    text = (
        "Artificial Intelligence is transforming healthcare "
        "by helping doctors diagnose diseases more accurately."
    )

    cached_summary = "Cached AI summary."

    cache_key = f"{text}:short"

    service.cache[cache_key] = {
        "summary": cached_summary,
        "created_at": __import__("time").time()
    }

    result = service.generate_summary(text, "short")

    assert result == cached_summary

    fake_client.models.generate_content.assert_not_called()

def test_generate_summary_cache_expired():
    fake_client = MagicMock()

    fake_client.models.generate_content.return_value.text = (
        "Fresh AI summary."
    )

    service = SummaryService.__new__(SummaryService)

    service.client = fake_client
    service.cache = {}
    service.cache_ttl = 300

    text = (
        "Artificial Intelligence is transforming healthcare "
        "by helping doctors diagnose diseases more accurately."
    )

    cache_key = f"{text}:short"

    service.cache[cache_key] = {
        "summary": "Old cached summary.",
        "created_at": __import__("time").time() - 600
    }

    result = service.generate_summary(text, "short")

    assert result == "Fresh AI summary."

    fake_client.models.generate_content.assert_called_once()

    assert service.cache[cache_key]["summary"] == "Fresh AI summary."

def test_generate_summary_gemini_failure():
    fake_client = MagicMock()

    fake_client.models.generate_content.side_effect = Exception(
        "Gemini service failed"
    )

    service = SummaryService.__new__(SummaryService)

    service.client = fake_client
    service.cache = {}
    service.cache_ttl = 300

    text = (
        "Artificial Intelligence is transforming healthcare "
        "by helping doctors diagnose diseases more accurately."
    )

    with pytest.raises(Exception, match="Gemini service failed"):
        service.generate_summary(text, "short")