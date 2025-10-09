from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class ReviewBase(BaseModel):
    user_id: int
    establishment_id: int
    rating: int                     
    comment: Optional[str] = None
    img: Optional[str] = None       

class ReviewCreate(ReviewBase):
    pass

class ReviewUpdate(BaseModel):
    rating: Optional[int] = None
    comment: Optional[str] = None
    img: Optional[str] = None

class ReviewOut(ReviewBase):
    resena_id: int                 
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class ReviewListOut(BaseModel):
    items: List[ReviewOut]

class MessageOut(BaseModel):
    msg: str
