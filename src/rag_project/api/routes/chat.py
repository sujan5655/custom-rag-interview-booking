
from uuid import uuid4

from fastapi import APIRouter, HTTPException, Request, Response

from rag_project.schemas.chat import ChatRequest, ChatResponse
from rag_project.services.rag_service import chat_with_documents
import logging
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post("/", response_model=ChatResponse)
async def chat(
    chat_request: ChatRequest,
    request: Request,
    response: Response,
) -> ChatResponse:
    try:
        # Get existing session from cookie
        session_id = request.cookies.get("session_id")

        # Create a new session if one doesn't exist
        if not session_id:
            session_id = str(uuid4())

        result = await chat_with_documents(
            session_id=session_id,
            question=chat_request.question,
            top_k=chat_request.top_k,
        )

        # Set an HTTP-only session cookie
        response.set_cookie(
            key="session_id",
            value=session_id,
            httponly=True,
            secure=False,  # Set True in production with HTTPS
            samesite="lax",
            max_age=86400,
            path="/",
        )
        result.pop("session_id", None)


        return ChatResponse(
            session_id=session_id,
            **result,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=422,
            detail=str(exc),
        ) from exc

    except Exception as exc:
      logger.exception("Chat API failed")
      raise HTTPException(
        status_code=500,
        detail="An error occurred while processing your question.",
    ) from exc