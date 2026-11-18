
from typing import Any

from rag_project.services.embedding_service import generate_query_embedding
from rag_project.services.vector_store_service import search_similar_chunks


async def retrieve_relevant_chunks(
    query: str,
    top_k: int = 5,
) -> list[dict[str, Any]]:
    if not query.strip():
        raise ValueError("Query cannot be empty")

    query_embedding = generate_query_embedding(query)

    results = await search_similar_chunks(
        query_embedding=query_embedding,
        limit=top_k,
    )

    return results
