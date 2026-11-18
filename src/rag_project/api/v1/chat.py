
from fastapi import APIRouter, HTTPException

from rag_project.schemas.chat import ChatRequest, ChatResponse
from rag_project.services.rag_service import chat_with_documents


router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post(
    "/",
    response_model=ChatResponse,
)
async def chat(request: ChatRequest) -> ChatResponse:
    try:
        result = await chat_with_documents(
            session_id=request.session_id,
            question=request.question,
            top_k=request.top_k,
        )

        return ChatResponse(**result)

    except ValueError as exc:
        raise HTTPException(
            status_code=422,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while processing your question.",
        ) from exc
