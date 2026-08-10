from app.utils.text import clean_text, remove_html_tags
from app.core.limiter import limiter

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

def test_summarize_text_too_short(client):

    response = client.post(
        "/v1/summarize",
        json={
            "text": "Too short",
            "style": "short"
        }
    )

    assert response.status_code == 422

    data = response.json()

    assert data["detail"][0]["type"] == "string_too_short"

def test_summarize_empty_text(client):

    response = client.post(
        "/v1/summarize",
        json={
            "text": "",
            "style": "short"
        }
    )

    assert response.status_code == 422

def test_summarize_invalid_style(client):

    response = client.post(
        "/v1/summarize",
        json={
            "text": (
                "Artificial Intelligence is transforming healthcare "
                "by helping doctors diagnose diseases more accurately."
            ),
            "style": "random"
        }
    )

    assert response.status_code == 422

    data = response.json()

    assert data["detail"][0]["type"] == "literal_error"

def test_clean_text():

    text = "   Artificial     Intelligence\n\nis\ttransforming   healthcare.   "

    result = clean_text(text)

    assert result == "Artificial Intelligence is transforming healthcare."


def test_remove_html_tags():

    text = "<h1>Hello</h1><p>Artificial Intelligence</p>"

    result = remove_html_tags(text)

    assert result == "Hello Artificial Intelligence"

def test_summarize_whitespace_only(client):

    response = client.post(
        "/v1/summarize",
        json={
            "text": "                         ",
            "style": "short"
        }
    )

    assert response.status_code == 422

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