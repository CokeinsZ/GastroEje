# app/routers/resenas.py
from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db

router = APIRouter(prefix="/resenas", tags=["Reseñas"])

# Crear una reseña → POST
@router.post("/")
async def create_resena(db: AsyncSession = Depends(get_db)):
    return {"msg": "Reseña creada correctamente"}

# Obtener todas las reseñas → GET
@router.get("/list")
async def list_resenas(db: AsyncSession = Depends(get_db)):
    return {"msg": "Lista de todas las reseñas"}

# Obtener reseñas de un establecimiento → GET
@router.get("/establecimiento/{establecimiento_id}")
async def get_resenas_by_establecimiento(
    establecimiento_id: int = Path(..., ge=1, description="ID del establecimiento"),
    db: AsyncSession = Depends(get_db),
):
    return {"msg": f"Reseñas del establecimiento {establecimiento_id}"}

# Obtener reseñas de un usuario → GET
@router.get("/usuario/{usuario_id}")
async def get_resenas_by_usuario(
    usuario_id: int = Path(..., ge=1, description="ID del usuario"),
    db: AsyncSession = Depends(get_db),
):
    return {"msg": f"Reseñas del usuario {usuario_id}"}

# Actualizar reseña → PUT
@router.put("/{resena_id}")
async def update_resena(
    resena_id: int = Path(..., ge=1, description="ID de la reseña"),
    db: AsyncSession = Depends(get_db),
):
    return {"msg": f"Reseña {resena_id} actualizada"}

# Eliminar reseña → DELETE
@router.delete("/{resena_id}")
async def delete_resena(
    resena_id: int = Path(..., ge=1, description="ID de la reseña"),
    db: AsyncSession = Depends(get_db),
):
    return {"msg": f"Reseña {resena_id} eliminada"}
