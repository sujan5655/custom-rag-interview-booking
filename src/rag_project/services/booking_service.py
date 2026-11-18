
import re
from datetime import date, time
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from rag_project.services.booking_memory_service import BookingMemory
from rag_project.services.booking_extraction_service import (
    extract_booking_details,
)
from rag_project.services.booking_database_service import (
    create_interview_booking,
)


REQUIRED_FIELDS = [
    "name",
    "email",
    "interview_date",
    "interview_time",
]


def format_booking_summary(booking: dict[str, Any]) -> str:
    return (
        "Please review your interview booking:\n\n"
        f"Name: {booking['name']}\n"
        f"Email: {booking['email']}\n"
        f"Date: {booking['interview_date']}\n"
        f"Time: {booking['interview_time']}\n\n"
        "Would you like me to confirm this booking?"
    )


def is_booking_rejection(message: str) -> bool:
    """Detect explicit rejection or cancellation of a booking."""

    message = message.lower().strip()

    rejection_patterns = [
        r"\bno,\s*i\s+(?:do\s+not|don't|dont)\s+want\s+to\s+confirm\b",
        r"\bi\s+(?:do\s+not|don't|dont)\s+want\s+to\s+confirm\b",
        r"\bi\s+(?:do\s+not|don't|dont)\s+want\s+to\s+proceed\b",
        r"\b(?:cancel|withdraw)\s+(?:this|the|my)\s+booking\b",
        r"\bno,\s*cancel\b",
    ]

    return any(
        re.search(pattern, message)
        for pattern in rejection_patterns
    )


async def process_booking_message(
    session_id: str,
    user_message: str,
    db: AsyncSession,
) -> dict[str, Any]:

    memory = BookingMemory(session_id)

    # 1. Get existing booking information
    booking = await memory.get_booking()

    # 2. Handle explicit booking rejection
    if booking and is_booking_rejection(user_message):
        await memory.clear_booking()

        return {
            "status": "cancelled",
            "message": (
                "Your interview booking request has been cancelled. "
                "No booking was created. You can start a new booking "
                "whenever you are ready."
            ),
            "booking": {},
        }

    # 3. Extract new information
    extracted = await extract_booking_details(user_message)

    new_details = extracted.details.model_dump(
        mode="json",
        exclude_none=True,
    )

    # 4. Merge new details with existing details
    booking.update(new_details)

    # 5. Check missing information
    missing_fields = [
        field
        for field in REQUIRED_FIELDS
        if not booking.get(field)
    ]

    # 6. Ask for missing information
    if missing_fields:
        await memory.save_booking(booking)

        field_questions = {
            "name": "What is your full name?",
            "email": "What is your email address?",
            "interview_date": "Which date would you prefer?",
            "interview_time": "What time would you prefer?",
        }

        question = field_questions[missing_fields[0]]

        return {
            "status": "collecting_information",
            "message": question,
            "booking": booking,
        }

    # 7. Validate interview date
    interview_date = date.fromisoformat(
        booking["interview_date"]
    )

    if interview_date < date.today():
        await memory.save_booking(booking)

        return {
            "status": "invalid_date",
            "message": (
                "The interview date must be today or in the future."
            ),
            "booking": booking,
        }

    # 8. Ask for confirmation
    if not extracted.confirmation_requested:
        await memory.save_booking(booking)

        return {
            "status": "awaiting_confirmation",
            "message": format_booking_summary(booking),
            "booking": booking,
        }

    # 9. Create PostgreSQL booking after confirmation
    try:
        created_booking = await create_interview_booking(
            db=db,
            name=booking["name"],
            email=booking["email"],
            interview_date=interview_date,
            interview_time=time.fromisoformat(
                booking["interview_time"]
            ),
        )

    except ValueError as exc:
        return {
            "status": "duplicate_booking",
            "message": str(exc),
            "booking": booking,
        }

    # 10. Clear temporary Redis booking information
    await memory.clear_booking()

    # 11. Return confirmed booking
    return {
        "status": "confirmed",
        "message": (
            "Your interview has been successfully booked!"
        ),
        "booking": {
            "id": str(created_booking.id),
            "name": created_booking.name,
            "email": created_booking.email,
            "interview_date": (
                created_booking.interview_date.isoformat()
            ),
            "interview_time": (
                created_booking.interview_time.isoformat()
            ),
            "status": created_booking.status,
        },
    }
