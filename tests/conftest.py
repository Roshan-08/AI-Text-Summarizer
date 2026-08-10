import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.dependencies import get_summary_service
from app.core.limiter import limiter


class MockSummaryService:

    def generate_summary(self, text, style):
        return "AI is transforming healthcare."

class FailingSummaryService:

    def generate_summary(self, text, style):
        raise Exception("Gemini service failed")

@pytest.fixture
def client():
    return TestClient(app, raise_server_exceptions=False)

@pytest.fixture
def mock_summary_service():

    service = MockSummaryService()

    app.dependency_overrides[
        get_summary_service
    ] = lambda: service

    yield service

    app.dependency_overrides.clear()

@pytest.fixture
def failing_summary_service():

    service = FailingSummaryService()

    app.dependency_overrides[
        get_summary_service
    ] = lambda: service

    yield service

    app.dependency_overrides.clear()

@pytest.fixture(autouse=True)
def reset_rate_limiter():
    limiter.reset()

    yield

    limiter.reset()