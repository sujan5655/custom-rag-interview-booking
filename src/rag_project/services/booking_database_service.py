
from datetime import date, time
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from rag_project.models.booking import InterviewBooking


async def create_interview_booking(
    db: AsyncSession,
    name: str,
    email: str,
    interview_date: date,
    interview_time: time,
) -> InterviewBooking:

    # Check for an existing booking at the same date and time
    statement = select(InterviewBooking).where(
        InterviewBooking.email == email,
        InterviewBooking.interview_date == interview_date,
        InterviewBooking.interview_time == interview_time,
        InterviewBooking.status == "confirmed",
    )

    result = await db.execute(statement)
    existing_booking = result.scalar_one_or_none()

    if existing_booking:
        raise ValueError(
            "You already have a confirmed booking for this time."
        )

    booking = InterviewBooking(
        name=name,
        email=email,
        interview_date=interview_date,
        interview_time=interview_time,
        status="confirmed",
    )

    db.add(booking)
    await db.commit()
    await db.refresh(booking)

    return booking
