from typing import Literal
from pydantic import BaseModel, Field, field_validator

class SummaryRequest(BaseModel):
    text: str = Field(
    ...,
    min_length=50,
    max_length=5000,
    description="Text that will be summarized by the AI model.",
    examples=[
        "Artificial Intelligence is transforming healthcare by helping doctors diagnose diseases more accurately."
    ]
)

    style: Literal["short", "bullet", "detailed"] = Field(
    default="short",
    description="Summary format to generate.",
    examples=["short"]
)

    @field_validator("text")
    @classmethod
    def validate_text(cls, value):
        if not value.strip():
            raise ValueError("Text cannot be empty.")
        return value


class SummaryResponse(BaseModel):

    summary: str = Field(
        ...,
        description="AI-generated summary of the input text."
    )

    word_count: int = Field(
        ...,
        description="Number of words in the generated summary."
    )

    model_used: str = Field(
        ...,
        description="Gemini model used to generate the summary."
    )

    processing_time_ms: float = Field(
        ...,
        description="Total time taken to generate the summary in milliseconds."
    )