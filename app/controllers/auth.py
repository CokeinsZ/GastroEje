from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from app.models.users import User
from app.schemas.auth import AuthBase
from app.utils.hashing import verify_password
from app.utils.jwt import create_access_token

async def authenticate_user(db: AsyncSession, user: AuthBase):
    """Autenticar al usuario y devolver el token JWT"""
    query = select(User).where(User.email == user.user)
    result = await db.execute(query)
    findUser = result.scalar_one_or_none()

    if not findUser or not verify_password(user.password, findUser.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Generar el token JWT
    token = create_access_token({"sub": findUser.email})
    return {
        "access_token": token,
        "token_type": "bearer"
    }
