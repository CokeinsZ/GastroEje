# app/routers/resenas.py
from fastapi import APIRouter, Depends, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.database import get_db
from app.schemas.review import ReviewCreate, ReviewUpdate, ReviewOut, MessageOut
from app.controllers import reviews as reviews_controller

router = APIRouter(prefix="/resenas", tags=["Reseñas"])

# Crear una reseña → POST
@router.post("/", response_model=ReviewOut, status_code=201)
async def create_resena(
    review: ReviewCreate,
    db: AsyncSession = Depends(get_db)
):
    """Crear una nueva reseña"""
    return await reviews_controller.create_review(db, review)

# Obtener todas las reseñas → GET
@router.get("/list", response_model=List[ReviewOut])
async def list_resenas(db: AsyncSession = Depends(get_db)):
    """Obtener lista de todas las reseñas"""
    return await reviews_controller.get_all_reviews(db)

# Obtener una reseña específica por usuario y establecimiento → GET
@router.get("/usuario/{user_id}/establecimiento/{establishment_id}", response_model=ReviewOut)
async def get_resena(
    user_id: int = Path(..., ge=1, description="ID del usuario"),
    establishment_id: int = Path(..., ge=1, description="ID del establecimiento"),
    db: AsyncSession = Depends(get_db),
):
    """Obtener una reseña específica por usuario y establecimiento"""
    return await reviews_controller.get_review_by_user_and_establishment(db, user_id, establishment_id)

# Obtener reseñas de un establecimiento → GET
@router.get("/establecimiento/{establecimiento_id}", response_model=List[ReviewOut])
async def get_resenas_by_establecimiento(
    establecimiento_id: int = Path(..., ge=1, description="ID del establecimiento"),
    db: AsyncSession = Depends(get_db),
):
    """Obtener todas las reseñas de un establecimiento específico"""
    return await reviews_controller.get_reviews_by_establishment(db, establecimiento_id)

# Obtener reseñas de un usuario → GET
@router.get("/usuario/{usuario_id}", response_model=List[ReviewOut])
async def get_resenas_by_usuario(
    usuario_id: int = Path(..., ge=1, description="ID del usuario"),
    db: AsyncSession = Depends(get_db),
):
    """Obtener todas las reseñas de un usuario específico"""
    return await reviews_controller.get_reviews_by_user(db, usuario_id)

# Actualizar reseña → PUT
@router.put("/usuario/{user_id}/establecimiento/{establishment_id}", response_model=ReviewOut)
async def update_resena(
    review: ReviewUpdate,
    user_id: int = Path(..., ge=1, description="ID del usuario"),
    establishment_id: int = Path(..., ge=1, description="ID del establecimiento"),
    db: AsyncSession = Depends(get_db),
):
    """Actualizar una reseña existente"""
    return await reviews_controller.update_review(db, user_id, establishment_id, review)

# Eliminar reseña → DELETE
@router.delete("/usuario/{user_id}/establecimiento/{establishment_id}", response_model=MessageOut)
async def delete_resena(
    user_id: int = Path(..., ge=1, description="ID del usuario"),
    establishment_id: int = Path(..., ge=1, description="ID del establecimiento"),
    db: AsyncSession = Depends(get_db),
):
    """Eliminar una reseña"""
    return await reviews_controller.delete_review(db, user_id, establishment_id)
