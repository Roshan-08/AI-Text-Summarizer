from fastapi import APIRouter, HTTPException
import logging
import time

from app.models.schemas import SummaryRequest, SummaryResponse
from app.services.summarizer import generate_summary

router = APIRouter()

logger = logging.getLogger(__name__)


@router.post("/v1/summarize", response_model=SummaryResponse)
def summarize(request: SummaryRequest):

    try:
        start_time = time.perf_counter()

        summary = generate_summary(request.text)

        end_time = time.perf_counter()

        logger.info(f"Summary generated in {end_time - start_time:.2f} seconds")

        processing_time_ms = round((end_time - start_time) * 1000, 2)

        return SummaryResponse(
            summary=summary,
            word_count=len(summary.split()),
            model_used="gemini-3.6-flash",
            processing_time_ms=processing_time_ms
        )

    except Exception as e:
        logger.error(f"Error generating summary: {e}")

        raise HTTPException(
            status_code=500,
            detail="Unable to generate summary. Please try again later."
        )