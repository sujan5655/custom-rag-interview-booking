
import asyncio
from pprint import pprint

from rag_project.db.database import AsyncSessionLocal
from rag_project.services.booking_memory_service import BookingMemory
from rag_project.services.booking_service import process_booking_message


async def main() -> None:
    session_id = "booking-database-test-001"

    memory = BookingMemory(session_id)
    await memory.clear_booking()

    async with AsyncSessionLocal() as db:

        first_result = await process_booking_message(
            session_id=session_id,
            user_message=(
                "My name is Sujan, my email is "
                "sujan@example.com. I want an interview "
                "on November 25, 2026 at 10:30 AM."
            ),
            db=db,
        )

        print("\nFirst response:")
        pprint(first_result)

        assert first_result["status"] == "awaiting_confirmation"

        second_result = await process_booking_message(
            session_id=session_id,
            user_message="Yes, I confirm this interview booking.",
            db=db,
        )

        print("\nSecond response:")
        pprint(second_result)

        assert second_result["status"] == "confirmed"
        assert second_result["booking"]["id"]

    await memory.clear_booking()

    print("\nPostgreSQL booking test passed!")


if __name__ == "__main__":
    asyncio.run(main())
