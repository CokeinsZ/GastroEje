from pydantic import BaseModel, ConfigDict

class MenuBase(BaseModel):
    title: str

class MenuCreate(MenuBase):
    establishment_id: int

class MenuUpdate(BaseModel):
    title: str | None = None

class MenuOut(MenuBase):
    menu_id: int
    establishment_id: int
    
    model_config = ConfigDict(from_attributes=True)

class MenuMessageOut(BaseModel):
    message: str