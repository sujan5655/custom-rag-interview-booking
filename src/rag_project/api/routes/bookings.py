
import uuid

from fastapi import APIRouter, Cookie, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession

from rag_project.core.config import settings
from rag_project.db.database import get_db
from rag_project.schemas.booking import (
    BookingChatRequest,
    BookingChatResponse,
)
from rag_project.services.booking_service import process_booking_message


router = APIRouter(
    prefix="/bookings",
    tags=["Interview Bookings"],
)


@router.post(
    "/chat",
    response_model=BookingChatResponse,
)
async def booking_chat(
    request: BookingChatRequest,
    response: Response,
    session_id: str | None = Cookie(default=None),
    db: AsyncSession = Depends(get_db),
) -> BookingChatResponse:

    # Generate a session for new conversations
    if session_id is None:
        session_id = str(uuid.uuid4())

    try:
        result = await process_booking_message(
            session_id=session_id,
            user_message=request.message,
            db=db,
        )

        # Set an HTTP-only cookie
        response.set_cookie(
            key="session_id",
            value=session_id,
            httponly=True,
            secure=not settings.DEBUG,
            samesite="lax",
            max_age=settings.REDIS_CHAT_TTL_SECONDS,
            path="/",
        )

        return BookingChatResponse(**result)

    except ValueError as exc:
        raise HTTPException(
            status_code=422,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Interview booking request failed.",
        ) from exc
