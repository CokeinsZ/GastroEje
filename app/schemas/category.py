from typing import Optional, List
from pydantic import BaseModel, ConfigDict

class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    """Body para crear categoría."""
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class CategoryOut(CategoryBase):
    category_id: int
    model_config = ConfigDict(from_attributes=True)

class CategoryListOut(BaseModel):
    items: List[CategoryOut]

class MessageOut(BaseModel):
    msg: str
