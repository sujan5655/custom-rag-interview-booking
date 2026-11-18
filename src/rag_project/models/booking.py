
import uuid

from sqlalchemy import Column, Date, DateTime, String, Time, func,  UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID

from rag_project.db.base import Base


class InterviewBooking(Base):
    __tablename__ = "interview_bookings"
    __table_args__ = (
    UniqueConstraint(
        "email",
        "interview_date",
        "interview_time",
        name="uq_interview_booking_email_date_time",
    ),
)


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
