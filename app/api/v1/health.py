from fastapi import APIRouter
from app.models.schemas import HealthResponse

router = APIRouter(
    prefix="/v1",
    tags=["Health"]
)

@router.get(
    "/health",
    response_model=HealthResponse,
    summary="API Health Check",
    description="""
Returns the current health status of the AI Text Summarizer API.

Use this endpoint to verify that the API is running and responding to requests.

### Response

A successful response returns:

- **status** — Current health status of the API.
""",
    response_description="API is healthy and operational."
)
def health():
    return {
        "status": "healthy"
    }