
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import text

from rag_project.core.config import settings
from rag_project.db.database import engine
from rag_project.integrations.redis import redis_client
from rag_project.integrations.qdrant import qdrant_client
from rag_project.api.routes.documents import router as documents_router
from rag_project.api.routes.chat import router as chat_router
from rag_project.api.routes.bookings import router as bookings_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    
    async with engine.connect() as connection:
        await connection.execute(text("SELECT 1"))

    await redis_client.ping()

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
    tags=["Documents"],
)

app.include_router(
    chat_router,
    prefix="/api/v1",
    tags=["Chat"],
)

app.include_router(
    bookings_router,
    prefix="/api/v1",
    tags=["Bookings"],
)

@app.get("/health")
async def health_check():

    services = {}

    try:
        async with engine.connect() as connection:
            await connection.execute(text("SELECT 1"))
        services["postgresql"] = "healthy"
    except Exception:
        services["postgresql"] = "unhealthy"

    try:
        await redis_client.ping()
        services["redis"] = "healthy"
    except Exception:
        services["redis"] = "unhealthy"

    try:
        await qdrant_client.get_collections()
        services["qdrant"] = "healthy"
    except Exception:
        services["qdrant"] = "unhealthy"

    is_healthy = all(
        status == "healthy"
        for status in services.values()
    )

    return {
        "status": "healthy" if is_healthy else "unhealthy",
        "services": services,
    }
