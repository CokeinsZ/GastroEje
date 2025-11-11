from typing import Optional, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
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
async def get_establishment_by_id(db: AsyncSession, establishment_id: int) -> Optional[Establishment]:
    query = select(Establishment).where(Establishment.id == establishment_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def get_establishments(db: AsyncSession, *, is_active: Optional[bool] = True) -> Sequence[Establishment]:
    query = select(Establishment)
    if is_active is not None:
        query = query.where(Establishment.is_active == is_active)
    result = await db.execute(query)
    return result.scalars().all()


# ---------- ACTUALIZAR ----------
async def update_establishment(
    db: AsyncSession, establishment_id: int, data: EstablishmentUpdate
) -> Optional[Establishment]:
    payload = data.model_dump(exclude_unset=True)
    if not payload:
        return await get_establishment_by_id(db, establishment_id)

    query = (
        update(Establishment)
        .where(Establishment.id == establishment_id)
        .values(**payload)
        .execution_options(synchronize_session="fetch")
    )
    await db.execute(query)
    await db.commit()
    return await get_establishment_by_id(db, establishment_id)


# ---------- ELIMINAR (borrado físico) ----------
async def delete_establishment(db: AsyncSession, establishment_id: int) -> bool:
    query = delete(Establishment).where(Establishment.id == establishment_id)
    result = await db.execute(query)
    await db.commit()
    return result.rowcount > 0
