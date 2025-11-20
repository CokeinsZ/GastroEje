from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database import get_db
from app.controllers.establishment import *
from app.schemas.establishment import EstablishmentCreate, EstablishmentUpdate, EstablishmentOut

router = APIRouter(prefix="/establishments", tags=["Establishments"])


# ---------- CREAR ----------
@router.post("/", response_model=EstablishmentOut)
async def create(data: EstablishmentCreate, db: AsyncSession = Depends(get_db)):
    return await create_establishment(db, data)





# ---------- LEER ----------
@router.get("/", response_model=List[EstablishmentOut])
async def list_all(db: AsyncSession = Depends(get_db)):
    return await get_establishments(db)





# ---------- LEER ----------
@router.get("/{establishment_id}", response_model=EstablishmentOut)
async def get_one(establishment_id: int, db: AsyncSession = Depends(get_db)):
    est = await get_establishment_by_id(db, establishment_id)
    if not est:
        raise HTTPException(status_code=404, detail="Establishment not found")
    return est


# ---------- ACTUALIZAR ----------
@router.patch("/{establishment_id}", response_model=EstablishmentOut)
async def update(establishment_id: int, data: EstablishmentUpdate, db: AsyncSession = Depends(get_db)):
    return await update_establishment(db, establishment_id, data)


# ---------- ELIMINAR ----------
@router.delete("/{establishment_id}")
async def delete(establishment_id: int, db: AsyncSession = Depends(get_db)):
    return await delete_establishment(db, establishment_id)
