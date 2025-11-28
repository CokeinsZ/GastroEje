from pydantic import BaseModel, ConfigDict
from datetime import datetime
from enum import Enum
from typing import Optional


class ReservationStatusEnum(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"

class ReservationsBase(BaseModel):
    user_id: int
    establishment_id: int
    date: datetime
    people_count: int

class ReservationsCreate(ReservationsBase):
    pass

class ReservationsUpdate(BaseModel):
    date: Optional[datetime] = None
    people_count: Optional[int] = None
    status: Optional[ReservationStatusEnum] = None

class ReservationsOut(ReservationsBase):
    reservation_id: int
    status: ReservationStatusEnum
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class MessageOut(BaseModel):
    message: str


