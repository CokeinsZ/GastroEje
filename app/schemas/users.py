from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional
from datetime import datetime
from app.models.users import UserRole, UserStatus

# Esquemas base
class UserBase(BaseModel):
    name: str
    last_name: Optional[str] = None
    email: EmailStr
    phone: Optional[str] = None
    role: UserRole
    status: UserStatus

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class ChangePassword(BaseModel):
    current_password: str
    new_password: str

class UpdateRole(BaseModel):
    role: UserRole

class UpdateStatus(BaseModel):
    status: UserStatus

# Esquemas de respuesta
class UserOut(UserBase):
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class UserLoginOut(BaseModel):
    message: str
    user_id: int
    access_token: str
    token_type: str = "bearer"

class UserMessageOut(BaseModel):
    message: str