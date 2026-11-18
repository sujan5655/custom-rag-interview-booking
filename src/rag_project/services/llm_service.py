
from typing import Any

from groq import AsyncGroq

from rag_project.core.config import settings


client = AsyncGroq(
    api_key=settings.GROQ_API_KEY,
)


async def generate_response(
    messages: list[dict[str, str]],
    temperature: float = 0.2,
    response_format: dict[str, str] | None = None,
) -> str:

    kwargs: dict[str, Any] = {
        "model": settings.GROQ_MODEL,
        "messages": messages,
        "temperature": temperature,
    }

    if response_format is not None:
        kwargs["response_format"] = response_format

    response = await client.chat.completions.create(**kwargs)

    content = response.choices[0].message.content

    if not content:
        raise RuntimeError("Groq returned an empty response")

    return content.strip()
