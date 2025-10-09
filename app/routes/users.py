from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.models.users import User, UserRole, UserStatus
from pydantic import BaseModel, EmailStr
from typing import List, Optional

router = APIRouter()

# Modelos Pydantic para request/response
class UserCreate(BaseModel):
    name: str
    last_name: Optional[str] = None
    email: EmailStr
    password: str
    phone: Optional[str] = None
    role: UserRole = UserRole.user

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None

class ChangePassword(BaseModel):
    current_password: str
    new_password: str

class UpdateRole(BaseModel):
    role: UserRole

class UpdateStatus(BaseModel):
    status: UserStatus

# Endpoints
@router.post("/register")
async def register_user(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    # Verificar si el email ya existe
    result = await db.execute(select(User).where(User.email == user_data.email))
    existing_user = result.scalar_one_or_none()
    
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Crear nuevo usuario (en producción hashear la contraseña)
    new_user = User(
        name=user_data.name,
        last_name=user_data.last_name,
        email=user_data.email,
        password=user_data.password,  # Hashear antes de guardar
        phone=user_data.phone,
        role=user_data.role
    )
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    return {"message": "User created successfully", "user_id": new_user.user_id}

@router.post("/login")
async def login_user(login_data: UserLogin, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == login_data.email))
    user = result.scalar_one_or_none()
    
    if not user or user.password != login_data.password:  # En producción usar BCrypt
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if user.status != UserStatus.ACTIVE:
        raise HTTPException(status_code=403, detail="User account is not active")
    
    return {"message": "Login successful", "user_id": user.user_id}

@router.get("/list")
async def list_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    users = result.scalars().all()
    return users

@router.get("/{user_id}")
async def get_user_by_id(
    user_id: int = Path(..., description="ID del usuario"),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(User).where(User.user_id == user_id))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user

@router.get("/email/{email}")
async def get_user_by_email(
    email: str = Path(..., description="Email del usuario"),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user

@router.put("/{user_id}")
async def update_user(
    user_data: UserUpdate,
    user_id: int = Path(..., description="ID del usuario a actualizar"),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(User).where(User.user_id == user_id))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Actualizar solo los campos proporcionados
    for field, value in user_data.dict(exclude_unset=True).items():
        setattr(user, field, value)
    
    await db.commit()
    await db.refresh(user)
    
    return {"message": "User updated successfully", "user": user}

@router.patch("/{user_id}/password")
async def change_password(
    password_data: ChangePassword,
    user_id: int = Path(..., description="ID del usuario"),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(User).where(User.user_id == user_id))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Verificar contraseña actual (en producción usar BCrypt)
    if user.password != password_data.current_password:
        raise HTTPException(status_code=401, detail="Current password is incorrect")
    
    # Actualizar contraseña (en producción hashear antes de guardar)
    user.password = password_data.new_password
    await db.commit()
    
    return {"message": "Password updated successfully"}

@router.patch("/{user_id}/allergens")
async def update_allergens(
    user_id: int = Path(..., description="ID del usuario"),
    db: AsyncSession = Depends(get_db)
):
    # Implementar lógica para actualizar alergias
    # Necesitarás un modelo Pydantic para las alergias
    return {"message": "Allergens updated successfully"}

@router.patch("/{user_id}/role")
async def change_role(
    role_data: UpdateRole,
    user_id: int = Path(..., description="ID del usuario"),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(User).where(User.user_id == user_id))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.role = role_data.role
    await db.commit()
    await db.refresh(user)
    
    return {"message": "Role updated successfully", "new_role": user.role}

@router.patch("/{user_id}/status")
async def change_status(
    status_data: UpdateStatus,
    user_id: int = Path(..., description="ID del usuario"),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(User).where(User.user_id == user_id))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.status = status_data.status
    await db.commit()
    await db.refresh(user)
    
    return {"message": "Status updated successfully", "new_status": user.status}

@router.delete("/{user_id}")
async def delete_user(
    user_id: int = Path(..., description="ID del usuario a eliminar"),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(User).where(User.user_id == user_id))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    await db.delete(user)
    await db.commit()
    
    return {"message": "User deleted successfully"}