from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.models.users import User, UserRole, UserStatus
from app.schemas.users import (
    UserCreate,
    UserUpdate,
    UserLogin,
    ChangePassword,
    UpdateRole,
    UpdateStatus,
    UserOut,
    UserLoginOut,
    UserMessageOut
)
from typing import List

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

# Endpoints
@router.post("/register", response_model=UserLoginOut, status_code=201)
async def register_user(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    """Registrar un nuevo usuario"""
    return {"message": "User created successfully", "user_id": 1}

@router.post("/login", response_model=UserLoginOut)
async def login_user(login_data: UserLogin, db: AsyncSession = Depends(get_db)):
    """Iniciar sesión de usuario"""
    return {"message": "Login successful", "user_id": 1}

@router.get("/list", response_model=List[UserOut])
async def list_users(db: AsyncSession = Depends(get_db)):
    """Obtener lista de todos los usuarios"""
    return []

@router.get("/{user_id}", response_model=UserOut)
async def get_user_by_id(
    user_id: int = Path(..., description="ID del usuario"),
    db: AsyncSession = Depends(get_db)
):
    """Obtener un usuario por su ID"""
    return {"user": "alsdfjaklsdf"}

@router.get("/email/{email}", response_model=UserOut)
async def get_user_by_email(
    email: str = Path(..., description="Email del usuario"),
    db: AsyncSession = Depends(get_db)
):
    """Obtener un usuario por su email"""
    return {"user": "alsdfjaklsdf"}

@router.put("/{user_id}", response_model=UserOut)
async def update_user(
    user_data: UserUpdate,
    user_id: int = Path(..., description="ID del usuario a actualizar"),
    db: AsyncSession = Depends(get_db)
):
    """Actualizar información de un usuario"""
    return {"message": "User updated successfully", "user": {}}

@router.patch("/{user_id}/password", response_model=UserMessageOut)
async def change_password(
    password_data: ChangePassword,
    user_id: int = Path(..., description="ID del usuario"),
    db: AsyncSession = Depends(get_db)
):
    """Cambiar la contraseña de un usuario"""
    return {"message": "Password updated successfully"}

@router.patch("/{user_id}/allergens", response_model=UserMessageOut)
async def update_allergens(
    user_id: int = Path(..., description="ID del usuario"),
    db: AsyncSession = Depends(get_db)
):
    """Actualizar alergias del usuario"""
    return {"message": "Allergens updated successfully"}

@router.patch("/{user_id}/role", response_model=UserMessageOut)
async def change_role(
    role_data: UpdateRole,
    user_id: int = Path(..., description="ID del usuario"),
    db: AsyncSession = Depends(get_db)
):
    """Cambiar el rol de un usuario"""
    return {"message": "Role updated successfully"}

@router.patch("/{user_id}/status", response_model=UserMessageOut)
async def change_status(
    status_data: UpdateStatus,
    user_id: int = Path(..., description="ID del usuario"),
    db: AsyncSession = Depends(get_db)
):
    """Cambiar el estado de un usuario"""
    return {"message": "Status updated successfully"}

@router.delete("/{user_id}", response_model=UserMessageOut)
async def delete_user(
    user_id: int = Path(..., description="ID del usuario a eliminar"),
    db: AsyncSession = Depends(get_db)
):
    """Eliminar un usuario"""
    return {"message": "User deleted successfully"}