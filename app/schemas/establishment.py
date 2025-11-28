from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime, time

class EstablishmentBase(BaseModel):
    NIT: str
    name: str
    description: Optional[str] = None
    sustainability_points: Optional[int] = None
    address: str
    mean_waiting_time: Optional[float] = None
    opening_hour: time
    closing_hour: time
    phone_number: Optional[str] = None
    website: Optional[str] = None
    logo: Optional[str] = None

class EstablishmentCreate(EstablishmentBase):
    pass

class EstablishmentUpdate(BaseModel):
    NIT: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    sustainability_points: Optional[int] = None
    address: Optional[str] = None
    mean_waiting_time: Optional[float] = None
    opening_hour: Optional[time] = None
    closing_hour: Optional[time] = None
    phone_number: Optional[str] = None
    website: Optional[str] = None
    logo: Optional[str] = None

class EstablishmentOut(EstablishmentBase):
    establishment_id: int
    model_config = ConfigDict(from_attributes=True)