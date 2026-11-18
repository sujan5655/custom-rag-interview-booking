
import json
from typing import Any

from rag_project.integrations.redis import redis_client
from rag_project.core.config import settings


class ConversationMemory:

    def __init__(self, session_id: str) -> None:
        self.session_id = session_id
        self.redis_key = f"chat:session:{session_id}:messages"

    async def get_history(self) -> list[dict[str, Any]]:
        messages = await redis_client.lrange(
            self.redis_key,
            0,
            -1,
        )

        return [
            json.loads(message)
            for message in messages
        ]

    async def add_message(
        self,
        role: str,
        content: str,
    ) -> None:
        if role not in {"user", "assistant"}:
            raise ValueError("Invalid message role")

        message = {
            "role": role,
            "content": content,
        }

        await redis_client.rpush(
            self.redis_key,
            json.dumps(message),
        )

        await redis_client.expire(
            self.redis_key,
            settings.REDIS_CHAT_TTL_SECONDS,
        )

    async def clear_history(self) -> None:
        await redis_client.delete(self.redis_key)
