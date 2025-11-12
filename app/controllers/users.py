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
    
    # Asegúrate de que `role` sea una cadena y conviértelo al enum UserRole
    try:
        role = UserRole[user_data.role]  # Convierte la cadena "user" o "admin" al enum correspondiente
    except KeyError:
        raise HTTPException(status_code=400, detail=f"Invalid role value: {user_data.role}")
    
    # Encriptar la contraseña antes de guardarla
    hashed_password = hash_password(user_data.password)
    
    # Crear el usuario
    new_user = User(
        email=user_data.email,
        password=hashed_password,
        name=user_data.name,
        last_name=user_data.last_name,  # Asegúrate de que este campo esté siendo usado si es necesario
        phone=user_data.phone,
        role="user",  # Asegúrate de que el role se esté pasando correctamente
        status="active",  # El valor del status ya debería coincidir con los valores del enum UserStatus
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    return UserLoginOut(message="User created successfully", user_id=new_user.id)

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
    
    return UserLoginOut(message="Login successful", user_id=user.id, access_token=token)

async def list_users_controller(db: AsyncSession) -> List[UserOut]:
    """Obtener lista de todos los usuarios"""
    query = select(User)
    result = await db.execute(query)
    users = result.scalars().all()
    
    return [UserOut(id=user.id, email=user.email, name=user.name) for user in users]

async def get_user_by_id_controller(user_id: int, db: AsyncSession) -> UserOut:
    """Obtener un usuario por su ID"""
    query = select(User).filter(User.id == user_id)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return UserOut(id=user.id, email=user.email, name=user.name)

async def get_user_by_email_controller(email: str, db: AsyncSession) -> UserOut:
    """Obtener un usuario por su email"""
    query = select(User).filter(User.email == email)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return UserOut(id=user.id, email=user.email, name=user.name)

async def update_user_controller(user_data: UserUpdate, user_id: int, db: AsyncSession) -> UserOut:
    """Actualizar información de un usuario"""
    query = select(User).filter(User.id == user_id)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.email = user_data.email
    user.name = user_data.name
    db.add(user)
    await db.commit()
    await db.refresh(user)
    
    return UserOut(id=user.id, email=user.email, name=user.name)

async def change_password_controller(password_data: ChangePassword, user_id: int, db: AsyncSession) -> UserMessageOut:
    """Cambiar la contraseña de un usuario"""
    query = select(User).filter(User.id == user_id)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Encriptar la nueva contraseña antes de guardarla
    hashed_password = hash_password(password_data.new_password)
    user.password = hashed_password
    db.add(user)
    await db.commit()
    
    return UserMessageOut(message="Password updated successfully")

async def update_allergens_controller(user_id: int, db: AsyncSession) -> UserMessageOut:
    """Actualizar alergias del usuario"""
    query = select(User).filter(User.id == user_id)
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
    query = select(User).filter(User.id == user_id)
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
    query = select(User).filter(User.id == user_id)
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
    query = select(User).filter(User.id == user_id)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    await db.delete(user)
    await db.commit()
    
    return UserMessageOut(message="User deleted successfully")
