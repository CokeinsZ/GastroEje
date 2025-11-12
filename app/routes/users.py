from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.controllers.users import change_password_controller, change_role_controller, change_status_controller, delete_user_controller, get_user_by_email_controller, get_user_by_id_controller, list_users_controller, register_user_controller, update_allergens_controller, update_user_controller
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
from app.utils.jwt import get_current_user  # Importar la función para obtener el usuario del token
from app.controllers.auth import authenticate_user  # Importar el controlador de autenticación

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

# Endpoints
@router.post("/register", response_model=UserLoginOut, status_code=201)
async def register_user(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    """Registrar un nuevo usuario"""
    # Lógica en el controlador
    return await register_user_controller(user_data, db)

@router.post("/login", response_model=UserLoginOut)
async def login_user(login_data: UserLogin, db: AsyncSession = Depends(get_db)):
    """Iniciar sesión de usuario"""
    # Lógica en el controlador
    return await authenticate_user(db, login_data)

@router.get("/list", response_model=List[UserOut])
async def list_users(db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    """Obtener lista de todos los usuarios"""
    # Lógica en el controlador
    return await list_users_controller(db)

@router.get("/{user_id}", response_model=UserOut)
async def get_user_by_id(
    user_id: int = Path(..., description="ID del usuario"),
    db: AsyncSession = Depends(get_db),
    current_user: str = Depends(get_current_user)  # Autenticación mediante JWT
):
    """Obtener un usuario por su ID"""
    # Lógica en el controlador
    return await get_user_by_id_controller(user_id, db)

@router.get("/email/{email}", response_model=UserOut)
async def get_user_by_email(
    email: str = Path(..., description="Email del usuario"),
    db: AsyncSession = Depends(get_db),
    current_user: str = Depends(get_current_user)  # Autenticación mediante JWT
):
    """Obtener un usuario por su email"""
    # Lógica en el controlador
    return await get_user_by_email_controller(email, db)

@router.put("/{user_id}", response_model=UserOut)
async def update_user(
    user_data: UserUpdate,
    user_id: int = Path(..., description="ID del usuario a actualizar"),
    db: AsyncSession = Depends(get_db),
    current_user: str = Depends(get_current_user)  # Autenticación mediante JWT
):
    """Actualizar información de un usuario"""
    # Lógica en el controlador
    return await update_user_controller(user_data, user_id, db)

@router.patch("/{user_id}/password", response_model=UserMessageOut)
async def change_password(
    password_data: ChangePassword,
    user_id: int = Path(..., description="ID del usuario"),
    db: AsyncSession = Depends(get_db),
    current_user: str = Depends(get_current_user)  # Autenticación mediante JWT
):
    """Cambiar la contraseña de un usuario"""
    # Lógica en el controlador
    return await change_password_controller(password_data, user_id, db)

@router.patch("/{user_id}/allergens", response_model=UserMessageOut)
async def update_allergens(
    user_id: int = Path(..., description="ID del usuario"),
    db: AsyncSession = Depends(get_db),
    current_user: str = Depends(get_current_user)  # Autenticación mediante JWT
):
    """Actualizar alergias del usuario"""
    # Lógica en el controlador
    return await update_allergens_controller(user_id, db)

@router.patch("/{user_id}/role", response_model=UserMessageOut)
async def change_role(
    role_data: UpdateRole,
    user_id: int = Path(..., description="ID del usuario"),
    db: AsyncSession = Depends(get_db),
    current_user: str = Depends(get_current_user)  # Autenticación mediante JWT
):
    """Cambiar el rol de un usuario"""
    # Lógica en el controlador
    return await change_role_controller(role_data, user_id, db)

@router.patch("/{user_id}/status", response_model=UserMessageOut)
async def change_status(
    status_data: UpdateStatus,
    user_id: int = Path(..., description="ID del usuario"),
    db: AsyncSession = Depends(get_db),
    current_user: str = Depends(get_current_user)  # Autenticación mediante JWT
):
    """Cambiar el estado de un usuario"""
    # Lógica en el controlador
    return await change_status_controller(status_data, user_id, db)

@router.delete("/{user_id}", response_model=UserMessageOut)
async def delete_user(
    user_id: int = Path(..., description="ID del usuario a eliminar"),
    db: AsyncSession = Depends(get_db),
    current_user: str = Depends(get_current_user)  # Autenticación mediante JWT
):
    """Eliminar un usuario"""
    # Lógica en el controlador
    return await delete_user_controller(user_id, db)
