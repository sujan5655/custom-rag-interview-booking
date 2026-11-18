
from functools import lru_cache

from sentence_transformers import SentenceTransformer

from rag_project.core.config import settings


@lru_cache(maxsize=1)
def get_embedding_model() -> SentenceTransformer:
    """Load and cache the embedding model."""

    return SentenceTransformer(
        settings.EMBEDDING_MODEL
    )


def generate_embeddings(
    texts: list[str],
) -> list[list[float]]:
    """Generate embeddings for multiple text chunks."""

    if not texts:
        return []

    model = get_embedding_model()

    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=False,
    )

    return embeddings.tolist()


def generate_query_embedding(
    text: str,
) -> list[float]:
    """Generate embedding for a user query."""

    embeddings = generate_embeddings([text])

    return embeddings[0]
