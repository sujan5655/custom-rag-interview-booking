
import asyncio
from rag_project.services.llm_service import generate_response


async def main() -> None:
    messages = [
        {
            "role": "system",
            "content": "You are a helpful AI assistant.",
        },
        {
            "role": "user",
            "content": "Explain RAG in simple words.",
        },
    ]

    response = await generate_response(messages)

    print("\nGroq response:\n")
    print(response)

    assert isinstance(response, str)
    assert len(response) > 0

    print("\nGroq integration test passed!")


if __name__ == "__main__":
    asyncio.run(main())
