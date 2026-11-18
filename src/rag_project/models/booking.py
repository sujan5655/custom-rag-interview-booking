
import uuid

from sqlalchemy import Column, Date, DateTime, String, Time, func
from sqlalchemy.dialects.postgresql import UUID

from rag_project.db.base import Base


class InterviewBooking(Base):
    __tablename__ = "interview_bookings"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    name = Column(
        String(150),
        nullable=False,
    )

    email = Column(
        String(255),
        nullable=False,
        index=True,
    )

    interview_date = Column(
        Date,
        nullable=False,
    )

    interview_time = Column(
        Time,
        nullable=False,
    )

    status = Column(
        String(30),
        nullable=False,
        default="confirmed",
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
