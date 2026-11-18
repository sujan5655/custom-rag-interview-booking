
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    session_id: str = Field(min_length=1, max_length=100)
    question: str = Field(min_length=1, max_length=5000)
    top_k: int = Field(default=5, ge=1, le=20)


class ChatResponse(BaseModel):
    session_id: str
    question: str
    answer: str
    retrieved_chunks: int
