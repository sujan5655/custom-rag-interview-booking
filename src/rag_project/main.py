
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import text

from rag_project.core.config import settings
from rag_project.db.database import engine
from rag_project.integrations.redis import redis_client
from rag_project.integrations.qdrant import qdrant_client
from rag_project.api.v1.documents import router as documents_router
from rag_project.api.v1.chat import router as chat_router
from rag_project.api.v1.bookings import router as bookings_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Verify PostgreSQL
    async with engine.connect() as connection:
        await connection.execute(text("SELECT 1"))

    # Verify Redis
    await redis_client.ping()

    # Verify Qdrant
    await qdrant_client.get_collections()

    print("All services connected successfully!")

    yield

    # Close connections
    await redis_client.aclose()
    await qdrant_client.close()
    await engine.dispose()



app = FastAPI(
    title=settings.APP_NAME,
    description="Document Ingestion and Conversational RAG API",
    version="1.0.0",
    lifespan=lifespan,
)


app.include_router(
    documents_router,
    prefix="/api/v1",
)

app.include_router(
    chat_router,
    prefix="/api/v1",
)

app.include_router(
    bookings_router,
    prefix="/api/v1",
)

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "services": [
            "FastAPI",
            "PostgreSQL",
            "Redis",
            "Qdrant",
        ],
    }
