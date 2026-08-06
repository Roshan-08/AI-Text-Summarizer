from fastapi import APIRouter, Depends, Request
from app.core.limiter import limiter
import logging
import time

from app.models.schemas import SummaryRequest, SummaryResponse
from app.dependencies import get_summary_service
from app.config.settings import MODEL_NAME
from app.validation.text_validator import validate_text
from app.models.api_response import APIResponse
from app.core.exceptions import InvalidInputException
from app.utils.text import clean_text

router = APIRouter(
    prefix="/v1",
    tags=["Summary"]
)

logger = logging.getLogger(__name__)


@router.post(
    "/summarize",
    response_model=APIResponse,
    summary="Generate AI Summary",
    description="Accepts text and returns an AI-generated summary using Gemini.",
    response_description="Successfully generated summary.",
    responses={
        400: {
            "description": "Bad Request - Invalid text input."
        },
        422: {
            "description": "Validation Error."
        },
        429: {
            "description": "Too Many Requests - Rate limit exceeded."
        },
        500: {
            "description": "Internal Server Error."
        }
    }
)

@limiter.limit("5/minute")
def summarize(
    request: Request,
    body: SummaryRequest,
    summary_service=Depends(get_summary_service)
) -> APIResponse:
    
    start_time = time.perf_counter()

    if not body.text:
        raise InvalidInputException(
            "Text cannot be empty"
        )

    cleaned_text = validate_text(body.text)

    cleaned_text = clean_text(cleaned_text)

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
        model_used=MODEL_NAME,
        processing_time_ms=processing_time_ms
    )

    return APIResponse(
        success=True,
        message="Summary generated successfully.",
        data=summary_response
    )