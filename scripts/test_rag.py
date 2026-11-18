
import asyncio
from pprint import pprint

from rag_project.services.rag_service import chat_with_documents


async def main() -> None:
    session_id = "rag-test-session-001"

    questions = [
        "What is the main topic of the uploaded document?",
        "Can you explain it in simple words?",
        "What are its important points?",
    ]

    for question in questions:
        print(f"\nUser: {question}")

        response = await chat_with_documents(
            session_id=session_id,
            question=question,
        )

        print("\nAssistant:")
        print(response["answer"])

        print(
            f"\nRetrieved chunks: "
            f"{response['retrieved_chunks']}"
        )

    print("\nCustom RAG pipeline test completed!")


if __name__ == "__main__":
    asyncio.run(main())
