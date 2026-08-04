from typing import Literal
from pydantic import BaseModel, Field, field_validator

class SummaryRequest(BaseModel):
    text: str = Field(..., min_length=50, max_length=5000)

    style: Literal["short", "bullet", "detailed"] = "short"

    @field_validator("text")
    @classmethod
    def validate_text(cls, value):
        if not value.strip():
            raise ValueError("Text cannot be empty.")
        return value


class SummaryResponse(BaseModel):
    summary: str
    word_count: int
    model_used: str
    processing_time_ms: float