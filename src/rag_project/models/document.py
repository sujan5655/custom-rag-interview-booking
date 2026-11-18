
import uuid

from sqlalchemy import Column, DateTime, Integer, String, func
from sqlalchemy.dialects.postgresql import UUID

from rag_project.db.base import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    filename = Column(
        String(255),
        nullable=False,
    )

    file_type = Column(
        String(10),
        nullable=False,
    )

    chunking_strategy = Column(
        String(50),
        nullable=False,
    )

    total_chunks = Column(
        Integer,
        nullable=False,
        default=0,
    )

    status = Column(
        String(30),
        nullable=False,
        default="pending",
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
