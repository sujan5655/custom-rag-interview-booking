
from typing import Any

from rag_project.services.llm_service import generate_response


async def rewrite_search_query(
    question: str,
    history: list[dict[str, Any]],
) -> str | None:
    if not history:
        return None

    messages = [
        {
            "role": "system",
            "content": (
                "You rewrite user questions into standalone document "
                "search queries using conversation history.\n\n"
                "Rules:\n"
                "1. Resolve references such as it, they, those, and them "
                "using the conversation history.\n"
                "2. If the question is understandable without previous "
                "conversation, return it as a standalone query.\n"
                "3. If the question cannot be understood because required "
                "context is missing, return exactly: NEED_CLARIFICATION\n"
                "4. Do not answer the question.\n"
                "5. Return only the rewritten query or "
                "NEED_CLARIFICATION."
            ),
        },
        *history,
        {
            "role": "user",
            "content": question,
        },
    ]

    rewritten_query = await generate_response(messages)

    rewritten_query = rewritten_query.strip()

    if rewritten_query == "NEED_CLARIFICATION":
        return None

    return rewritten_query or None
