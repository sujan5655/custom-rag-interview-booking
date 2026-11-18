
import json
from typing import Any

from rag_project.integrations.redis import redis_client
from rag_project.core.config import settings


class BookingMemory:

    def __init__(self, session_id: str) -> None:
        self.redis_key = f"booking:session:{session_id}"

    async def get_booking(self) -> dict[str, Any]:
        data = await redis_client.get(self.redis_key)

        if not data:
            return {}

        return json.loads(data)

    async def save_booking(
        self,
        booking_data: dict[str, Any],
    ) -> None:
        await redis_client.set(
            self.redis_key,
            json.dumps(booking_data),
            ex=settings.REDIS_CHAT_TTL_SECONDS,
        )

    async def clear_booking(self) -> None:
        await redis_client.delete(self.redis_key)
