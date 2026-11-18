import logging
import uuid
from pathlib import Path

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from rag_project.models.document import Document
from rag_project.schemas.document import ChunkingStrategy
from rag_project.services.extraction_service import extract_document_text
from rag_project.services.chunking_service import chunk_document
from rag_project.services.embedding_service import generate_embeddings
from rag_project.services.vector_store_service import (
    create_collection,
    store_embeddings,
)

logger = logging.getLogger(__name__)


async def ingest_document(
    db: AsyncSession,
    file_path: Path,
    filename: str,
    strategy: ChunkingStrategy,
) -> Document:

    document = Document(
        id=uuid.uuid4(),
        filename=filename,
        file_type=Path(filename).suffix.lower(),
        chunking_strategy=strategy,
        total_chunks=0,
        status="processing",
    )

    db.add(document)
    await db.commit()
    await db.refresh(document)
    document_id = document.id

    try:
        # 1. Extract text
        text = extract_document_text(file_path)

        # 2. Generate chunks
        chunks = chunk_document(
            text=text,
            strategy=strategy,
            chunk_size=500,
            overlap=100,
        )

        if not chunks:
            raise ValueError("No chunks generated.")

        # 3. Generate embeddings
        embeddings = generate_embeddings(chunks)

        # 4. Store vectors
        await create_collection()
        await store_embeddings(
            document_id=document.id,
            filename=filename,
            chunks=chunks,
            embeddings=embeddings,
        )

        # 5. Update metadata
        document.total_chunks = len(chunks)
        document.status = "completed"

        await db.commit()
        await db.refresh(document)

        return document

    except Exception:
        logger.exception("Document ingestion failed for %s", filename)
        await db.rollback()
        await db.execute(
            update(Document)
            .where(Document.id == document_id)
            .values(status="failed")
        )
        await db.commit()
        raise