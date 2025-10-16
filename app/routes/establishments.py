# app/routers/establecimientos.py
from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.database import get_db
from app.schemas.establishment import EstablishmentCreate, EstablishmentOut
from app.schemas.category import MessageOut

router = APIRouter(prefix="/establecimientos", tags=["Establecimientos"])

# Listar establecimientos → GET
@router.get("/list", response_model=List[EstablishmentOut])
async def list_establecimientos(db: AsyncSession = Depends(get_db)):
    """Obtener lista de todos los establecimientos"""
    return []

# Eliminar establecimientos → DELETE
@router.delete("/{establecimiento_id}", response_model=MessageOut)
async def delete_establecimiento(
    establecimiento_id: int = Path(..., ge=1, description="ID del establecimiento"),
    db: AsyncSession = Depends(get_db),
):
    """Eliminar un establecimiento"""
    return {"msg": f"Establecimiento {establecimiento_id} eliminado"}

# Actualizar info → POST (endpoint separado para mantener el verbo POST que pediste)
@router.post("/{establecimiento_id}/actualizar", response_model=EstablishmentOut)
async def actualizar_info_establecimiento(
    establishment: EstablishmentCreate,
    establecimiento_id: int = Path(..., ge=1, description="ID del establecimiento"),
    db: AsyncSession = Depends(get_db),
):
    """Actualizar información de un establecimiento"""
    return {"msg": f"Información del establecimiento {establecimiento_id} actualizada"}

# Mostrar info del establecimiento → GET
@router.get("/{establecimiento_id}", response_model=EstablishmentOut)
async def get_establecimiento(
    establecimiento_id: int = Path(..., ge=1, description="ID del establecimiento"),
    db: AsyncSession = Depends(get_db),
):
    """Obtener información de un establecimiento específico"""
    return {"msg": f"Información del establecimiento {establecimiento_id}"}

# Registrar establecimiento → POST
@router.post("/", response_model=EstablishmentOut, status_code=201)
async def registrar_establecimiento(
    establishment: EstablishmentCreate,
    db: AsyncSession = Depends(get_db)
):
    """Registrar un nuevo establecimiento"""
    return {"msg": "Establecimiento registrado correctamente"}
