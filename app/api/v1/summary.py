from fastapi import APIRouter, Depends
import logging
import time

from app.models.schemas import SummaryRequest, SummaryResponse
from app.dependencies import get_summary_service
from app.config.settings import MODEL_NAME
from app.validation.text_validator import validate_text

router = APIRouter(
    prefix="/v1",
    tags=["Summary"]
)

logger = logging.getLogger(__name__)


@router.post(
    "/summarize",
    response_model=SummaryResponse,
    summary="Generate AI Summary",
    description="Accepts text and returns an AI-generated summary using Gemini.",
    response_description="Successfully generated summary."
)
def summarize(
    request: SummaryRequest,
    summary_service=Depends(get_summary_service)
):
    start_time = time.perf_counter()

    cleaned_text = validate_text(request.text)

    summary = summary_service.generate_summary(
        cleaned_text,
        request.style
)

    end_time = time.perf_counter()

    logger.info(
        f"Summary generated in {end_time - start_time:.2f} seconds"
    )

    processing_time_ms = round(
        (end_time - start_time) * 1000,
        2
    )

    return SummaryResponse(
        summary=summary,
        word_count=len(summary.split()),
        model_used=MODEL_NAME,
        processing_time_ms=processing_time_ms
    )