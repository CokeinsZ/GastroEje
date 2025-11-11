from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_session
from app.controllers.establishment import *
from app.schemas.establishment import EstablishmentCreate, EstablishmentUpdate

router = APIRouter(prefix="/establishments", tags=["Establishments"])


# ---------- CREAR ----------
@router.post("/")
async def create(data: EstablishmentCreate, db: AsyncSession = Depends(get_session)):
    return await create_establishment(db, data)





# ---------- LEER ----------
@router.get("/")
async def list_all(db: AsyncSession = Depends(get_session)):
    return await get_establishments(db)





# ---------- LEER ----------
@router.get("/{establishment_id}")
async def get_one(establishment_id: int, db: AsyncSession = Depends(get_session)):
    return await get_establishment_by_id(db, establishment_id)


# ---------- ACTUALIZAR ----------
@router.patch("/{establishment_id}")
async def update(establishment_id: int, data: EstablishmentUpdate, db: AsyncSession = Depends(get_session)):
    return await update_establishment(db, establishment_id, data)


# ---------- ELIMINAR ----------
@router.delete("/{establishment_id}")
async def delete(establishment_id: int, db: AsyncSession = Depends(get_session)):
    return await delete_establishment(db, establishment_id)
