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
    service.cache_max_size = 100

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

    cache_key = service._build_cache_key(text, "short")

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

    cache_key = service._build_cache_key(text, "short")

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
    service.cache_max_size = 100

    text = (
        "Artificial Intelligence is transforming healthcare "
        "by helping doctors diagnose diseases more accurately."
    )

    cache_key = service._build_cache_key(text, "short")

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

def test_cache_key_is_sha256_hash():

    service = SummaryService.__new__(SummaryService)

    text = (
        "Artificial Intelligence is transforming healthcare "
        "by helping doctors diagnose diseases more accurately."
    )

    cache_key = service._build_cache_key(text, "short")

    assert len(cache_key) == 64
    assert cache_key == cache_key.lower()

    assert text not in cache_key
    assert "short" not in cache_key


def test_cache_key_changes_with_text_or_style():

    service = SummaryService.__new__(SummaryService)

    text = (
        "Artificial Intelligence is transforming healthcare "
        "by helping doctors diagnose diseases more accurately."
    )

    same_text_same_style = service._build_cache_key(text, "short")
    different_style = service._build_cache_key(text, "detailed")
    different_text = service._build_cache_key(
        text + " This is additional information.",
        "short"
    )

    assert same_text_same_style != different_style
    assert same_text_same_style != different_text


def test_cache_does_not_exceed_max_size():

    fake_client = MagicMock()

    fake_client.models.generate_content.return_value.text = (
        "AI summary."
    )

    service = SummaryService.__new__(SummaryService)

    service.client = fake_client
    service.cache = {}
    service.cache_ttl = 300
    service.cache_max_size = 3

    texts = [
        "Artificial Intelligence is transforming healthcare by improving diagnosis.",
        "Machine Learning helps businesses analyze large amounts of useful data.",
        "Cloud computing provides scalable infrastructure for modern applications.",
        "Cybersecurity protects systems and data from unauthorized access."
    ]

    for text in texts:
        service.generate_summary(text, "short")

    assert len(service.cache) == 3
