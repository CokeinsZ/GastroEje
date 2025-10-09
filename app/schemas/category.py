from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, constr

class CategoryBase(BaseModel):
    name : str
    description : str

class CategoryCreate(CategoryBase):
    pass

class