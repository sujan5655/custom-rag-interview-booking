
import asyncio
from pprint import pprint

from rag_project.services.retrieval_service import retrieve_relevant_chunks


async def main() -> None:
    query = "What is the main topic of the uploaded document?"

    results = await retrieve_relevant_chunks(
        query=query,
        top_k=5,
    )

    print(f"Retrieved {len(results)} chunks:\n")

    for result in results:
        pprint(result)
        print("-" * 60)

    assert isinstance(results, list)

    if results:
        assert "payload" in results[0]
        assert "text" in results[0]["payload"]

    print("\nQdrant retrieval test completed!")


if __name__ == "__main__":
    asyncio.run(main())
