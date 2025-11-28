from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from enum import Enum


class RatingEnum(str, Enum):
    ONE = "1"
    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"


class ReviewBase(BaseModel):
    rating: str  # Usando RatingEnum como string
    comment: Optional[str] = None
    img: Optional[str] = None


class ReviewCreate(ReviewBase):
    user_id: int
    establishment_id: int


class ReviewUpdate(BaseModel):
    rating: Optional[str] = None
    comment: Optional[str] = None
    img: Optional[str] = None


class ReviewOut(ReviewBase):
    user_id: int
    establishment_id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class MessageOut(BaseModel):
    message: str
