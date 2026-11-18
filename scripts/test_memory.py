
import asyncio

from rag_project.services.memory_service import ConversationMemory


async def main() -> None:
    memory = ConversationMemory("test-session-001")

    await memory.clear_history()

    await memory.add_message(
        "user",
        "What is Python?",
    )

    await memory.add_message(
        "assistant",
        "Python is a programming language.",
    )

    await memory.add_message(
        "user",
        "What are its applications?",
    )

    history = await memory.get_history()

    for message in history:
        print(message)

    assert len(history) == 3
    assert history[0]["role"] == "user"
    assert history[1]["role"] == "assistant"
    assert history[2]["content"] == "What are its applications?"

    print("\nRedis conversation memory test passed!")

    await memory.clear_history()


if __name__ == "__main__":
    asyncio.run(main())
