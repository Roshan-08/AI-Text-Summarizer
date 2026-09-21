from fastapi import APIRouter, Depends, Request
from app.core.limiter import limiter
import logging
import time

from app.models.schemas import SummaryRequest, SummaryResponse
from app.dependencies import get_summary_service
from app.config.settings import settings
from app.validation.text_validator import validate_text
from app.models.api_response import APIResponse
from app.utils.text import clean_text, remove_html_tags

router = APIRouter(
    prefix="/v1",
    tags=["Summary"]
)

logger = logging.getLogger(__name__)


@router.post(
    "/summarize",
    response_model=APIResponse[SummaryResponse],
    summary="Generate AI Summary",
    description="""
Generates an AI-powered summary from the provided text using Google Gemini.

### Supported summary styles

- **short** — Concise paragraph summary.
- **bullet** — Key points presented as bullet points.
- **detailed** — More comprehensive summary containing additional context.

### Processing

The API performs the following steps:

1. Validates the input text.
2. Removes HTML tags.
3. Normalizes whitespace.
4. Generates the summary using Google Gemini.
5. Returns summary metadata and processing time.

### Rate Limit

Maximum **5 requests per minute** per client.
""",
    response_description="Successfully generated summary.",
    responses={
        200: {
            "description": "Summary generated successfully.",
            "content": {
                "application/json": {
                    "example": {
                        "success": True,
                        "message": "Summary generated successfully.",
                        "data": {
                            "summary": "Artificial Intelligence is transforming healthcare by improving disease diagnosis.",
                            "word_count": 9,
                            "model_used": "gemini-3.6-flash",
                            "processing_time_ms": 1250.42
                        }
                    }
                }
            }
        },
        400: {
            "description": "Bad Request - Invalid text input.",
            "content": {
                "application/json": {
                    "example": {
                        "success": False,
                        "message": "Text is too short for summarization.",
                        "data": None
                    }
                }
            }
        },
        422: {
            "description": "Validation Error - Request body does not match the expected schema.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "loc": ["body", "text"],
                                "msg": "Field required",
                                "type": "missing"
                            }
                        ]
                    }
                }
            }
        },
        429: {
            "description": "Too Many Requests - Rate limit exceeded.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "5 per 1 minute"
                    }
                }
            }
        },
        500: {
            "description": "Internal Server Error - An unexpected error occurred.",
            "content": {
                "application/json": {
                    "example": {
                        "success": False,
                        "message": "Internal server error.",
                        "data": None
                    }
                }
            }
        }
    }
)

@limiter.limit("5/minute")
def summarize(
    request: Request,
    body: SummaryRequest,
    summary_service=Depends(get_summary_service)
) -> APIResponse[SummaryResponse]:
    
    start_time = time.perf_counter()


    cleaned_text = validate_text(body.text)

    cleaned_text = remove_html_tags(cleaned_text)
    logger.info(f"After HTML removal: {cleaned_text}")

    cleaned_text = clean_text(cleaned_text)
    logger.info(f"After whitespace cleanup: {cleaned_text}")

    summary = summary_service.generate_summary(
        cleaned_text,
        body.style
)

    end_time = time.perf_counter()

    logger.info(
        f"Summary generated in {end_time - start_time:.2f} seconds"
    )

    processing_time_ms = round(
        (end_time - start_time) * 1000,
        2
    )

    summary_response = SummaryResponse(
        summary=summary,
        word_count=len(summary.split()),
        model_used=settings.model_name,
        processing_time_ms=processing_time_ms
    )

    return APIResponse(
        success=True,
        message="Summary generated successfully.",
        data=summary_response
    )