
import pytest

from rag_project.services.chunking_service import (
    fixed_size_chunking,
    recursive_chunking,
    chunk_document,
)


SAMPLE_TEXT = """
Python is a programming language.

FastAPI is a modern Python framework.
It is used to build APIs.

Redis is an in-memory database.
Qdrant is a vector database.
"""


def test_fixed_size_chunking():
    chunks = fixed_size_chunking(
        SAMPLE_TEXT,
        chunk_size=50,
        overlap=10,
    )

    assert len(chunks) > 1
    assert all(len(chunk) <= 50 for chunk in chunks)


def test_recursive_chunking():
    chunks = recursive_chunking(
        SAMPLE_TEXT,
        chunk_size=50,
        overlap=10,
    )

    assert len(chunks) > 1
    assert all(chunk.strip() for chunk in chunks)


def test_chunking_selector():
    chunks = chunk_document(
        text=SAMPLE_TEXT,
        strategy="fixed_size",
    )

    assert isinstance(chunks, list)
    assert len(chunks) > 0


def test_invalid_chunk_size():
    with pytest.raises(ValueError):
        fixed_size_chunking(
            SAMPLE_TEXT,
            chunk_size=0,
        )


def test_invalid_overlap():
    with pytest.raises(ValueError):
        recursive_chunking(
            SAMPLE_TEXT,
            chunk_size=100,
            overlap=100,
        )
