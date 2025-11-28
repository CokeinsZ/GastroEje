from typing import List
import bcrypt
from sqlalchemy import insert, update, delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

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

# Función para encriptar contraseñas
def hash_password(password: str) -> str:
    """Generar un hash para una contraseña."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# Función para verificar contraseñas
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verificar si la contraseña en texto claro coincide con el hash almacenado."""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))



async def register_user_controller(user_data: UserCreate, db: AsyncSession) -> UserLoginOut:
    """Registrar un nuevo usuario"""
    # Verificar si el email ya está en uso
    query = select(User).filter(User.email == user_data.email)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Encriptar la contraseña antes de guardarla
    hashed_password = hash_password(user_data.password)
    
    # Crear el usuario
    new_user = User(
        email=user_data.email,
        password=hashed_password,
        name=user_data.name,
        last_name=user_data.last_name,
        phone=user_data.phone,
        role=user_data.role,  # user_data.role ya es un enum UserRole
        status=user_data.status,  # user_data.status ya es un enum UserStatus
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    from app.utils.jwt import create_access_token
    token = create_access_token({"sub": new_user.email})
    
    return UserLoginOut(message="User created successfully", user_id=new_user.user_id, access_token=token)

async def login_user_controller(login_data: UserLogin, db: AsyncSession) -> UserLoginOut:
    """Iniciar sesión de usuario y generar un token JWT"""
    query = select(User).filter(User.email == login_data.email)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    
    if not user or not verify_password(login_data.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid email or password")
    
    # Aquí generas el token JWT para el usuario autenticado
    from app.utils.jwt import create_access_token
    token = create_access_token({"sub": user.email})
    
    return UserLoginOut(message="Login successful", user_id=user.user_id, access_token=token)

async def list_users_controller(db: AsyncSession) -> List[UserOut]:
    """Obtener lista de todos los usuarios"""
    query = select(User)
    result = await db.execute(query)
    users = result.scalars().all()
    
    return [UserOut.model_validate(user) for user in users]

async def get_user_by_id_controller(user_id: int, db: AsyncSession) -> UserOut:
    """Obtener un usuario por su ID"""
    query = select(User).filter(User.user_id == user_id)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return UserOut.model_validate(user)

async def get_user_by_email_controller(email: str, db: AsyncSession) -> UserOut:
    """Obtener un usuario por su email"""
    query = select(User).filter(User.email == email)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return UserOut.model_validate(user)

async def update_user_controller(user_data: UserUpdate, user_id: int, db: AsyncSession) -> UserOut:
    """Actualizar información de un usuario"""
    query = select(User).filter(User.user_id == user_id)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Actualizar solo los campos proporcionados
    if user_data.name is not None:
        user.name = user_data.name
    if user_data.last_name is not None:
        user.last_name = user_data.last_name
    if user_data.phone is not None:
        user.phone = user_data.phone
    
    db.add(user)
    await db.commit()
    await db.refresh(user)
    
    return UserOut.model_validate(user)

async def change_password_controller(password_data: ChangePassword, user_id: int, db: AsyncSession) -> UserMessageOut:
    """Cambiar la contraseña de un usuario"""
    query = select(User).filter(User.user_id == user_id)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Verificar la contraseña actual
    if not verify_password(password_data.current_password, user.password):
        raise HTTPException(status_code=400, detail="Current password is incorrect")
    
    # Encriptar la nueva contraseña antes de guardarla
    hashed_password = hash_password(password_data.new_password)
    user.password = hashed_password
    db.add(user)
    await db.commit()
    
    return UserMessageOut(message="Password updated successfully")

async def update_allergens_controller(user_id: int, db: AsyncSession) -> UserMessageOut:
    """Actualizar alergias del usuario"""
    query = select(User).filter(User.user_id == user_id)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Aquí agregarías la lógica para actualizar las alergias del usuario
    # user.allergens = updated_allergens_data
    db.add(user)
    await db.commit()
    
    return UserMessageOut(message="Allergens updated successfully")

async def change_role_controller(role_data: UpdateRole, user_id: int, db: AsyncSession) -> UserMessageOut:
    """Cambiar el rol de un usuario"""
    query = select(User).filter(User.user_id == user_id)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.role = role_data.role
    db.add(user)
    await db.commit()
    
    return UserMessageOut(message="Role updated successfully")

async def change_status_controller(status_data: UpdateStatus, user_id: int, db: AsyncSession) -> UserMessageOut:
    """Cambiar el estado de un usuario"""
    query = select(User).filter(User.user_id == user_id)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.status = status_data.status
    db.add(user)
    await db.commit()
    
    return UserMessageOut(message="Status updated successfully")

async def delete_user_controller(user_id: int, db: AsyncSession) -> UserMessageOut:
    """Eliminar un usuario"""
    query = select(User).filter(User.user_id == user_id)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    await db.delete(user)
    await db.commit()
    
    return UserMessageOut(message="User deleted successfully")
