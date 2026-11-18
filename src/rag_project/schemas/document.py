import uuid
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


ChunkingStrategy = Literal["fixed_size", "recursive"]


class DocumentUploadResponse(BaseModel):
    document_id: uuid.UUID = Field(validation_alias="id")
    filename: str
    file_type: str
    chunking_strategy: ChunkingStrategy
    total_chunks: int
    status: str
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )