import logging
from pathlib import Path
from tempfile import NamedTemporaryFile

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from rag_project.core.config import settings
from rag_project.db.database import get_db
from rag_project.schemas.document import (
    ChunkingStrategy,
    DocumentUploadResponse,
)
from rag_project.services.document_service import ingest_document
from rag_project.services.extraction_service import DocumentExtractionError

logger = logging.getLogger(__name__)


router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)

ALLOWED_EXTENSIONS = {".pdf", ".txt"}


@router.post(
    "/upload",
    response_model=DocumentUploadResponse,
    status_code=201,
)
async def upload_document(
    file: UploadFile = File(...),
    chunking_strategy: ChunkingStrategy = Form(...),
    db: AsyncSession = Depends(get_db),
) -> DocumentUploadResponse:

    filename = Path(file.filename or "").name
    extension = Path(filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and TXT files are supported.",
        )

    if not filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is required.",
        )

    temp_path: Path | None = None

    try:
        max_upload_bytes = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
        file_size = 0

        with NamedTemporaryFile(
            suffix=extension,
            delete=False,
        ) as temp_file:
            temp_path = Path(temp_file.name)
            while chunk := await file.read(1024 * 1024):
                file_size += len(chunk)
                if file_size > max_upload_bytes:
                    raise HTTPException(
                        status_code=413,
                        detail=(
                            "File size cannot exceed "
                            f"{settings.MAX_UPLOAD_SIZE_MB} MB."
                        ),
                    )
                temp_file.write(chunk)
            temp_file.flush()

        if file_size == 0:
            raise HTTPException(
                status_code=400,
                detail="Uploaded file is empty.",
            )

        document = await ingest_document(
            db=db,
            file_path=temp_path,
            filename=filename,
            strategy=chunking_strategy,
        )

        return DocumentUploadResponse(
            document_id=document.id,
            filename=document.filename,
            file_type=document.file_type,
            chunking_strategy=document.chunking_strategy,
            total_chunks=document.total_chunks,
            status=document.status,
            created_at=document.created_at,
        )

    except HTTPException:
        raise

    except DocumentExtractionError as exc:
        raise HTTPException(
            status_code=422,
            detail=str(exc),
        ) from exc

    except ValueError as exc:
        raise HTTPException(
            status_code=422,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        logger.exception("Document ingestion failed")
        raise HTTPException(
            status_code=500,
            detail=str(exc) if settings.DEBUG else "Document ingestion failed.",
        ) from exc

    finally:
        if temp_path and temp_path.exists():
            temp_path.unlink()

        await file.close()