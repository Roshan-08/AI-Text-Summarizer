import pytest

from app.main import app
from app.core.limiter import limiter
from app.utils.text import clean_text, remove_html_tags

@pytest.mark.parametrize(
    "text",
    [
        "Too short",
        "",
        "       ",
    ]
)
def test_summarize_invalid_text(client, text):

    response = client.post(
        "/v1/summarize",
        json={
            "text": text,
            "style": "short"
        }
    )

    assert response.status_code == 422


def test_summarize_missing_text(client):

    response = client.post(
        "/v1/summarize",
        json={
            "style": "short"
        }
    )

    assert response.status_code == 422

    data = response.json()

    assert "detail" in data
    assert isinstance(data["detail"], list)
    assert len(data["detail"]) > 0

    error = data["detail"][0]

    assert error["type"] == "missing"
    assert "text" in error["loc"]

def test_summarize_missing_style(client, mock_summary_service):

    response = client.post(
        "/v1/summarize",
        json={
            "text": (
                "Artificial Intelligence is transforming healthcare "
                "by helping doctors diagnose diseases more accurately."
            )
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert data["message"] == "Summary generated successfully."
    assert data["data"]["summary"] == "AI is transforming healthcare."

def test_summarize_invalid_text_type(client):

    response = client.post(
        "/v1/summarize",
        json={
            "text": 12345,
            "style": "short"
        }
    )

    assert response.status_code == 422

    data = response.json()

    assert "detail" in data
    assert isinstance(data["detail"], list)
    assert len(data["detail"]) > 0

    error = data["detail"][0]

    assert error["type"] == "string_type"
    assert "text" in error["loc"]

def test_summarize_invalid_body(client):

    response = client.post(
        "/v1/summarize",
        json=["this", "is", "not", "an", "object"]
    )

    assert response.status_code == 422

    data = response.json()

    assert "detail" in data
    assert isinstance(data["detail"], list)
    assert len(data["detail"]) > 0

    error = data["detail"][0]

    assert error["type"] == "model_attributes_type"

def test_summarize_success(client, mock_summary_service):

    response = client.post(
        "/v1/summarize",
        json={
            "text": (
                "Artificial Intelligence is transforming healthcare "
                "by helping doctors diagnose diseases more accurately."
            ),
            "style": "short"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert data["message"] == "Summary generated successfully."
    assert data["data"]["summary"] == "AI is transforming healthcare."

def test_summary_does_not_log_user_text(client, mock_summary_service, caplog):

    sensitive_text = (
        "This is a confidential document that should never appear in application logs."
    )

    with caplog.at_level("INFO"):

        response = client.post(
            "/v1/summarize",
            json={
                "text": sensitive_text,
                "style": "short"
            }
        )

    assert response.status_code == 200

    for record in caplog.records:
        assert sensitive_text not in record.getMessage()


@pytest.mark.parametrize(
    "style",
    [
        "random",
        "medium",
        "very_long",
    ]
)
def test_summarize_invalid_style(client, style):

    response = client.post(
        "/v1/summarize",
        json={
            "text": (
                "Artificial Intelligence is transforming healthcare "
                "by helping doctors diagnose diseases more accurately."
            ),
            "style": style
        }
    )

    assert response.status_code == 422

    data = response.json()

    assert data["detail"][0]["type"] == "literal_error"

def test_clean_text():

    text = "   Artificial     Intelligence\n\nis\ttransforming   healthcare.   "

    result = clean_text(text)

    assert result == "Artificial Intelligence is transforming healthcare."

def test_validate_text_success():
    from app.validation.text_validator import validate_text

    text = (
        "   Artificial Intelligence is transforming healthcare "
        "by helping doctors diagnose diseases more accurately.   "
    )

    result = validate_text(text)

    assert result == (
        "Artificial Intelligence is transforming healthcare "
        "by helping doctors diagnose diseases more accurately."
    )
def test_summary_request_valid_text():
    from app.models.schemas import SummaryRequest

    request = SummaryRequest(
        text=(
            "Artificial Intelligence is transforming healthcare "
            "by helping doctors diagnose diseases more accurately."
        )
    )

    assert request.text.startswith("Artificial Intelligence")
    assert request.style == "short"


def test_remove_html_tags():

    text = "<h1>Hello</h1><p>Artificial Intelligence</p>"

    result = remove_html_tags(text)

    assert result == "Hello Artificial Intelligence"


def test_summarize_rate_limit(client, mock_summary_service):

    payload = {
        "text": (
            "Artificial Intelligence is transforming healthcare "
            "by helping doctors diagnose diseases more accurately."
        ),
        "style": "short"
    }

    responses = []

    for _ in range(6):
        response = client.post(
            "/v1/summarize",
            json=payload
        )
        responses.append(response)

    assert responses[-1].status_code == 429

    # Reset rate limiter after intentionally exhausting the limit
    limiter.reset()

def test_summarize_service_failure(client, failing_summary_service):

    response = client.post(
        "/v1/summarize",
        json={
            "text": (
                "Artificial Intelligence is transforming healthcare "
                "by helping doctors diagnose diseases more accurately."
            ),
            "style": "short"
        }
    )

    assert response.status_code == 500

    data = response.json()

    assert data["success"] is False
    assert data["message"] == "An internal server error occurred."
    assert data["error_code"] == "INTERNAL_SERVER_ERROR"
    assert data["data"] is None

def test_service_failure_does_not_leak_internal_error(
    client,
    failing_summary_service
):

    sensitive_error = "Gemini API key SECRET-123 failed at C:\\internal\\service.py"

    response = client.post(
        "/v1/summarize",
        json={
            "text": (
                "Artificial Intelligence is transforming healthcare "
                "by helping doctors diagnose diseases more accurately."
            ),
            "style": "short"
        }
    )

    assert response.status_code == 500

    response_text = response.text

    assert "SECRET-123" not in response_text
    assert "C:\\internal\\service.py" not in response_text
    assert "Gemini service failed" not in response_text
    assert "An internal server error occurred." in response_text

def test_invalid_input_exception(client):
    from app.core.exceptions import InvalidInputException
    from app.dependencies import get_summary_service

    def failing_dependency():
        raise InvalidInputException("Text input is invalid.")

    app = client.app

    app.dependency_overrides[get_summary_service] = failing_dependency

    try:
        response = client.post(
            "/v1/summarize",
            json={
                "text": (
                    "Artificial Intelligence is transforming healthcare "
                    "by helping doctors diagnose diseases more accurately."
                ),
                "style": "short"
            }
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 400

    data = response.json()

    assert data["success"] is False
    assert data["message"] == "Text input is invalid."
    assert data["error_code"] == "INVALID_INPUT"
    assert data["data"] is None

def test_summarize_response_structure(client, mock_summary_service):

    response = client.post(
        "/v1/summarize",
        json={
            "text": (
                "Artificial Intelligence is transforming healthcare "
                "by helping doctors diagnose diseases more accurately."
            ),
            "style": "short"
        }
    )

    assert response.status_code == 200

    data = response.json()

    # Top-level API response contract
    assert set(data.keys()) == {
        "success",
        "message",
        "data"
    }

    # Summary response contract
    assert set(data["data"].keys()) == {
        "summary",
        "model_used",
        "word_count",
        "processing_time_ms"
    }

    assert isinstance(data["success"], bool)
    assert isinstance(data["message"], str)

    assert isinstance(data["data"]["summary"], str)
    assert isinstance(data["data"]["model_used"], str)
    assert isinstance(data["data"]["word_count"], int)
    assert isinstance(data["data"]["processing_time_ms"], (int, float))

def test_validation_error_response_structure(client):
    response = client.post(
        "/v1/summarize",
        json={
            "text": "Too short",
            "style": "short"
        }
    )

    assert response.status_code == 422

    data = response.json()

    assert "detail" in data
    assert isinstance(data["detail"], list)
    assert len(data["detail"]) > 0

    error = data["detail"][0]

    assert "type" in error
    assert "loc" in error
    assert "msg" in error

def test_invalid_input_exception_response_structure(client):
    from app.core.exceptions import InvalidInputException
    from app.dependencies import get_summary_service

    def failing_dependency():
        raise InvalidInputException("Text input is invalid.")

    app.dependency_overrides[get_summary_service] = failing_dependency

    try:
        response = client.post(
            "/v1/summarize",
            json={
                "text": (
                    "Artificial Intelligence is transforming healthcare "
                    "by helping doctors diagnose diseases more accurately."
                ),
                "style": "short"
            }
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 400

    data = response.json()

    assert set(data.keys()) == {
        "success",
        "message",
        "error_code",
        "data"
    }

    assert isinstance(data["success"], bool)
    assert isinstance(data["message"], str)
    assert isinstance(data["error_code"], str)
    assert data["data"] is None

def test_rate_limit_response_structure(client, mock_summary_service):

    payload = {
        "text": (
            "Artificial Intelligence is transforming healthcare "
            "by helping doctors diagnose diseases more accurately."
        ),
        "style": "short"
    }

    responses = []

    for _ in range(6):
        response = client.post(
            "/v1/summarize",
            json=payload
        )
        responses.append(response)

    response = responses[-1]

    assert response.status_code == 429

    data = response.json()

    assert "detail" in data
    assert isinstance(data["detail"], str)

    limiter.reset()

def test_summary_request_empty_text():
    from app.models.schemas import SummaryRequest

    with pytest.raises(ValueError, match="Text cannot be empty."):
        SummaryRequest(
            text=" " * 50
        )

def test_validate_text_too_short():
    from fastapi import HTTPException
    from app.validation.text_validator import validate_text

    with pytest.raises(HTTPException) as exc_info:
        validate_text("Too short")

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Text is too short for summarization."


def test_validate_text_too_long():
    from fastapi import HTTPException
    from app.validation.text_validator import validate_text
    from app.config.settings import settings

    text = "a" * (settings.max_input_length + 1)

    with pytest.raises(HTTPException) as exc_info:
        validate_text(text)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Text exceeds the maximum allowed length."

def test_validate_text_accepts_maximum_length():
    from app.validation.text_validator import validate_text
    from app.config.settings import settings

    text = ("word " * 10).strip()

    remaining = settings.max_input_length - len(text)

    text += "a" * remaining

    result = validate_text(text)

    assert len(result) == settings.max_input_length
    assert len(result.split()) >= 10
