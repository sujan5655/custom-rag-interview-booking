
import uuid
from typing import Any

from qdrant_client import models

from rag_project.core.config import settings
from rag_project.integrations.qdrant import qdrant_client


async def create_collection() -> None:
    """Create the Qdrant collection if it doesn't exist."""

    collections = await qdrant_client.get_collections()

    collection_names = [
        collection.name
        for collection in collections.collections
    ]

    if settings.QDRANT_COLLECTION in collection_names:
        return

    await qdrant_client.create_collection(
        collection_name=settings.QDRANT_COLLECTION,
        vectors_config=models.VectorParams(
            size=settings.EMBEDDING_DIMENSION,
            distance=models.Distance.COSINE,
        ),
    )


async def store_embeddings(
    document_id: uuid.UUID,
    filename: str,
    chunks: list[str],
    embeddings: list[list[float]],
) -> None:
    """Store document chunks and embeddings in Qdrant."""

    if len(chunks) != len(embeddings):
        raise ValueError(
            "Number of chunks and embeddings must match."
        )

    if not chunks:
        return

    points = []

    for index, (chunk, embedding) in enumerate(
        zip(chunks, embeddings, strict=True)
    ):
        point_id = str(
            uuid.uuid5(
                document_id,
                str(index),
            )
        )

        points.append(
            models.PointStruct(
                id=point_id,
                vector=embedding,
                payload={
                    "document_id": str(document_id),
                    "filename": filename,
                    "chunk_index": index,
                    "text": chunk,
                },
            )
        )

    await qdrant_client.upsert(
        collection_name=settings.QDRANT_COLLECTION,
        points=points,
        wait=True,
    )


async def search_similar_chunks(
    query_embedding: list[float],
    limit: int = 5,
) -> list[dict[str, Any]]:
    """Retrieve relevant document chunks."""

    if limit <= 0:
        raise ValueError("limit must be greater than zero.")

    response = await qdrant_client.query_points(
        collection_name=settings.QDRANT_COLLECTION,
        query=query_embedding,
        limit=limit,
        with_payload=True,
    )

    results = []

    for point in response.points:
        results.append(
            {
                "id": str(point.id),
                "score": point.score,
                "payload": point.payload,
            }
        )

    return results
