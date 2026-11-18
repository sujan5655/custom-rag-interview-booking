
from qdrant_client import AsyncQdrantClient

from rag_project.core.config import settings


qdrant_client = AsyncQdrantClient(
    url=settings.QDRANT_URL,
)


async def get_qdrant() -> AsyncQdrantClient:
    return qdrant_client
