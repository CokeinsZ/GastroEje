from pydantic import BaseModel, ConfigDict
from datetime import datetime
from enum import Enum


class ReservationStatusEnum(str, Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"

class ReservationsBase(BaseModel):
    reservation_id: int
    user_id: int
    establishment_id: int
    date: datetime
    people_count: int
    status: ReservationStatusEnum
    created_at: datetime
    updated_at: datetime

class ReservationsCreate(ReservationsBase):
    pass

class ReservationsOut(ReservationsBase):
    id_reservation: int  
    model_config = ConfigDict(from_attributes=True)


