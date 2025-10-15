from pydantic import BaseModel, ConfigDict
from typing import Optional

class DishBase(BaseModel):
    menu_id: int
    name: str
    description: Optional[str] = None
    price: float
    img: Optional[str] = None

class DishCreate(DishBase):
    pass

class DishOut(DishBase):
    dish_id: int
    model_config = ConfigDict(from_attributes=True)