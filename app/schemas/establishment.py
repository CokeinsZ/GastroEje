from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class EstablishmentBase(BaseModel):
    name: str
    description: Optional[str] = None
    sustainability_points: Optional[int] = None
    address: str
    mean_waiting_time: Optional[float] = None
    opening_hour: datetime
    closing_hour: datetime
    phone_number: Optional[str] = None
    website: Optional[str] = None
    logo: Optional[str] = None

class EstablishmentCreate(EstablishmentBase):
    pass

class EstablishmentOut(EstablishmentBase):
    establishment_id: int
    model_config = ConfigDict(from_attributes=True)