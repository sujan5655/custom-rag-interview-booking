
import asyncio

from rag_project.services.booking_memory_service import BookingMemory


async def main() -> None:
    memory = BookingMemory("booking-test-001")

    await memory.clear_booking()

    booking = {
        "name": "Sujan",
        "email": "sujan@example.com",
        "interview_date": "2026-11-25",
        "interview_time": "10:30:00",
    }

    await memory.save_booking(booking)

    saved_booking = await memory.get_booking()

    print("Saved booking:")
    print(saved_booking)

    assert saved_booking["name"] == "Sujan"
    assert saved_booking["email"] == "sujan@example.com"
    assert saved_booking["interview_date"] == "2026-11-25"

    print("\nBooking memory test passed!")

    await memory.clear_booking()


if __name__ == "__main__":
    asyncio.run(main())
