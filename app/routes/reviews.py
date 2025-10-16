# app/routers/resenas.py
from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.database import get_db
from app.schemas.review import ReviewCreate, ReviewUpdate, ReviewOut, ReviewListOut, MessageOut

router = APIRouter(prefix="/resenas", tags=["Reseñas"])

# Crear una reseña → POST
@router.post("/", response_model=ReviewOut, status_code=201)
async def create_resena(
    review: ReviewCreate,
    db: AsyncSession = Depends(get_db)
):
    """Crear una nueva reseña"""
    return {"msg": "Reseña creada correctamente"}

# Obtener todas las reseñas → GET
@router.get("/list", response_model=ReviewListOut)
async def list_resenas(db: AsyncSession = Depends(get_db)):
    """Obtener lista de todas las reseñas"""
    return {"items": []}

# Obtener reseñas de un establecimiento → GET
@router.get("/establecimiento/{establecimiento_id}", response_model=ReviewListOut)
async def get_resenas_by_establecimiento(
    establecimiento_id: int = Path(..., ge=1, description="ID del establecimiento"),
    db: AsyncSession = Depends(get_db),
):
    """Obtener todas las reseñas de un establecimiento específico"""
    return {"items": []}

# Obtener reseñas de un usuario → GET
@router.get("/usuario/{usuario_id}", response_model=ReviewListOut)
async def get_resenas_by_usuario(
    usuario_id: int = Path(..., ge=1, description="ID del usuario"),
    db: AsyncSession = Depends(get_db),
):
    """Obtener todas las reseñas de un usuario específico"""
    return {"items": []}

# Actualizar reseña → PUT
@router.put("/{resena_id}", response_model=ReviewOut)
async def update_resena(
    review: ReviewUpdate,
    resena_id: int = Path(..., ge=1, description="ID de la reseña"),
    db: AsyncSession = Depends(get_db),
):
    """Actualizar una reseña existente"""
    return {"msg": f"Reseña {resena_id} actualizada"}

# Eliminar reseña → DELETE
@router.delete("/{resena_id}", response_model=MessageOut)
async def delete_resena(
    resena_id: int = Path(..., ge=1, description="ID de la reseña"),
    db: AsyncSession = Depends(get_db),
):
    """Eliminar una reseña"""
    return {"msg": f"Reseña {resena_id} eliminada"}
