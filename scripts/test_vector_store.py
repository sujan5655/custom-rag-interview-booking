
import asyncio
import uuid

from rag_project.services.embedding_service import (
    generate_embeddings,
    generate_query_embedding,
)
from rag_project.services.vector_store_service import (
    create_collection,
    store_embeddings,
    search_similar_chunks,
)


async def main() -> None:
    # Sample document
    document_id = uuid.uuid4()

    chunks = [
        "Python is a programming language.",
        "FastAPI is used to build REST APIs.",
        "Qdrant is a vector database used for similarity search.",
        "Redis is an in-memory data store.",
    ]

    # 1. Create collection
    await create_collection()
    print("Qdrant collection ready!")

    # 2. Generate embeddings
    embeddings = generate_embeddings(chunks)
    print("Embeddings generated!")

    # 3. Store vectors
    await store_embeddings(
        document_id=document_id,
        filename="sample.txt",
        chunks=chunks,
        embeddings=embeddings,
    )
    print("Vectors stored successfully!")

    # 4. Search similar chunks
    query = "What is used to build REST APIs?"

    query_embedding = generate_query_embedding(query)

    results = await search_similar_chunks(
        query_embedding=query_embedding,
        limit=3,
    )

    print("\nSearch results:")

    for result in results:
        print("\nScore:", result["score"])
        print("Text:", result["payload"]["text"])
        print("Filename:", result["payload"]["filename"])

    assert len(results) > 0

    print("\nQdrant integration test passed!")


if __name__ == "__main__":
    asyncio.run(main())
