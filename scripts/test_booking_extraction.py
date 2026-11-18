
import asyncio
from pprint import pprint

from rag_project.services.booking_extraction_service import (
    extract_booking_details,
)


async def main() -> None:
    message = (
        "My name is Sujan, my email is "
        "sujan@example.com. I want an interview "
        "on November 25, 2026 at 10:30 AM."
    )

    result = await extract_booking_details(message)

    print("\nExtracted booking details:")
    pprint(result.model_dump(mode="json"))

    assert result.details.name == "Sujan"
    assert str(result.details.email) == "sujan@example.com"
    assert result.details.interview_date is not None
    assert result.details.interview_time is not None

    print("\nBooking extraction test passed!")


if __name__ == "__main__":
    asyncio.run(main())
