from pydantic import BaseModel, ConfigDict

class AllergenBase(BaseModel):
    name: str

class AllergenCreate(AllergenBase):
    pass

class AllergenUpdate(BaseModel):
    name: str | None = None

class AllergenOut(AllergenBase):
    allergen_id: int
    
    model_config = ConfigDict(from_attributes=True)

class AllergenMessageOut(BaseModel):
    message: str