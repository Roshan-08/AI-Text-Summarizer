import pytest
from pydantic import ValidationError

from app.config.settings import Settings


def test_settings_requires_gemini_api_key():
    with pytest.raises(ValidationError):
        Settings(_env_file=None)


def test_settings_rejects_invalid_cache_ttl():
    with pytest.raises(ValidationError):
        Settings(
            GEMINI_API_KEY="test",
            CACHE_TTL="-10"
        )


def test_settings_rejects_invalid_max_input_length():
    with pytest.raises(ValidationError):
        Settings(
            GEMINI_API_KEY="test",
            MAX_INPUT_LENGTH="0"
        )


def test_settings_accepts_valid_configuration():
    settings = Settings(
        GEMINI_API_KEY="test",
        MODEL_NAME="test-model",
        CACHE_TTL="600",
        MAX_INPUT_LENGTH="10000"
    )

    assert settings.gemini_api_key == "test"
    assert settings.model_name == "test-model"
    assert settings.cache_ttl == 600
    assert settings.max_input_length == 10000