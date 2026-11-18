
from datetime import date, time
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class BookingDetails(BaseModel):
    name: Optional[str] = Field(default=None, max_length=150)
    email: Optional[EmailStr] = None
    interview_date: Optional[date] = None
    interview_time: Optional[time] = None


class BookingExtraction(BaseModel):
    details: BookingDetails
    confirmation_requested: bool = False


class BookingResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    interview_date: date
    interview_time: time
    status: str

    model_config = ConfigDict(from_attributes=True)




from datetime import date, time
from typing import Any

from pydantic import BaseModel, Field


from typing import Any

from pydantic import BaseModel, Field


class BookingChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=5000)


class BookingChatResponse(BaseModel):
    status: str
    message: str
    booking: dict[str, Any] = {}



