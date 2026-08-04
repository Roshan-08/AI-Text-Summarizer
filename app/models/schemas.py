from pydantic import BaseModel

class SummaryRequest(BaseModel):
    text: str

class SummaryResponse(BaseModel):
    summary: str
    word_count: int
    model_used: str
    processing_time_ms: float