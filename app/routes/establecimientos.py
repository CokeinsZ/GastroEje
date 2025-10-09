# app/routers/establecimientos.py
from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db

router = APIRouter(prefix="/establecimientos", tags=["Establecimientos"])

# Listar establecimientos → GET
@router.get("/list")
async def list_establecimientos(db: AsyncSession = Depends(get_db)):
    return {"msg": "Lista de todos los establecimientos"}

# Eliminar establecimientos → DELETE
@router.delete("/{establecimiento_id}")
async def delete_establecimiento(
    establecimiento_id: int = Path(..., ge=1, description="ID del establecimiento"),
    db: AsyncSession = Depends(get_db),
):
    return {"msg": f"Establecimiento {establecimiento_id} eliminado"}

# Actualizar info → POST (endpoint separado para mantener el verbo POST que pediste)
@router.post("/{establecimiento_id}/actualizar")
async def actualizar_info_establecimiento(
    establecimiento_id: int = Path(..., ge=1, description="ID del establecimiento"),
    db: AsyncSession = Depends(get_db),
):
    return {"msg": f"Información del establecimiento {establecimiento_id} actualizada"}

# Mostrar info del establecimiento → GET
@router.get("/{establecimiento_id}")
async def get_establecimiento(
    establecimiento_id: int = Path(..., ge=1, description="ID del establecimiento"),
    db: AsyncSession = Depends(get_db),
):
    return {"msg": f"Información del establecimiento {establecimiento_id}"}

# Registrar establecimiento → POST
@router.post("/")
async def registrar_establecimiento(db: AsyncSession = Depends(get_db)):
    return {"msg": "Establecimiento registrado correctamente"}
