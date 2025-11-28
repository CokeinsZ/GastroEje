from typing import Optional, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from fastapi import HTTPException
from app.models.establishments import Establishment
from app.schemas.establishment import EstablishmentCreate, EstablishmentUpdate


# ---------- CREAR ----------
async def create_establishment(db: AsyncSession, data: EstablishmentCreate) -> Establishment:
    est = Establishment(**data.model_dump())
    db.add(est)
    await db.flush()       # asigna ID
    await db.refresh(est)  # trae valores por defecto
    await db.commit()
    return est


# ---------- LEER ----------
async def get_establishment_by_id(db: AsyncSession, establishment_id: int) -> Establishment:
    query = select(Establishment).where(Establishment.establishment_id == establishment_id)
    result = await db.execute(query)
    establishment = result.scalar_one_or_none()
    if not establishment:
        raise HTTPException(status_code=404, detail="Establishment not found")
    return establishment


async def get_establishments(db: AsyncSession) -> Sequence[Establishment]:
    query = select(Establishment)
    result = await db.execute(query)
    return result.scalars().all()


# ---------- ACTUALIZAR ----------
async def update_establishment(
    db: AsyncSession, establishment_id: int, data: EstablishmentUpdate
) -> Establishment:
    # Verificar que exista
    establishment = await get_establishment_by_id(db, establishment_id)
    
    payload = data.model_dump(exclude_unset=True)
    if not payload:
        return establishment

    query = (
        update(Establishment)
        .where(Establishment.establishment_id == establishment_id)
        .values(**payload)
        .execution_options(synchronize_session="fetch")
    )
    await db.execute(query)
    await db.commit()
    return await get_establishment_by_id(db, establishment_id)


# ---------- ELIMINAR (borrado físico) ----------
async def delete_establishment(db: AsyncSession, establishment_id: int) -> dict:
    # Verificar que exista
    await get_establishment_by_id(db, establishment_id)
    
    query = delete(Establishment).where(Establishment.establishment_id == establishment_id)
    await db.execute(query)
    await db.commit()
    return {"message": "Establishment deleted successfully"}
