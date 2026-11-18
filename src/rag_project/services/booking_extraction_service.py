
import json
from datetime import date

from pydantic import ValidationError

from rag_project.schemas.booking import BookingExtraction
from rag_project.services.llm_service import generate_response


BOOKING_EXTRACTION_PROMPT = """
You are an interview booking information extraction assistant.

Extract booking information from the user's latest message.

Required fields:
- name
- email
- interview_date
- interview_time

Rules:
1. Extract only information explicitly provided or clearly stated
   in the latest user message.
2. Do not invent missing information.
3. Return null for fields not provided in the latest message.
4. Use ISO format YYYY-MM-DD for interview_date.
5. Use 24-hour HH:MM:SS format for interview_time.
6. Resolve relative dates using the supplied current date.
7. Set confirmation_requested to true only when the user
   explicitly agrees to confirm the booking.
8. A question or an expression of interest is not confirmation.
9. Return only valid JSON with this structure:

{
    "details": {
        "name": null,
        "email": null,
        "interview_date": null,
        "interview_time": null
    },
    "confirmation_requested": false
}
"""


async def extract_booking_details(
    user_message: str,
) -> BookingExtraction:

    if not user_message.strip():
        raise ValueError("User message cannot be empty")

    messages = [
        {
            "role": "system",
            "content": BOOKING_EXTRACTION_PROMPT,
        },
        {
            "role": "user",
            "content": (
                f"Current date: {date.today().isoformat()}\n"
                f"Latest user message: {user_message}"
            ),
        },
    ]

    response = await generate_response(
    messages=messages,
    temperature=0,
    response_format={"type": "json_object"},
)

    try:
        extracted_data = json.loads(response)
        return BookingExtraction.model_validate(extracted_data)

    except (json.JSONDecodeError, ValidationError) as exc:
        raise ValueError(
            "Could not extract valid booking information"
        ) from exc
