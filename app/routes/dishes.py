# app/routers/platos.py
from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.database import get_db
from app.schemas.dishes import DishCreate, DishOut
from app.schemas.category import MessageOut

router = APIRouter(prefix="/platos", tags=["Platos"])

# Listar platos → GET
@router.get("/list", response_model=List[DishOut])
async def list_platos(db: AsyncSession = Depends(get_db)):
    """Obtener lista de todos los platos"""
    return []

# Mostrar info de un plato → GET
@router.get("/{plato_id}", response_model=DishOut)
async def get_plato(
    plato_id: int = Path(..., ge=1, description="ID del plato"),
    db: AsyncSession = Depends(get_db),
):
    """Obtener información de un plato específico"""
    return {"msg": f"Información del plato {plato_id}"}

# Modificar o actualizar plato → PUT
@router.put("/{plato_id}", response_model=DishOut)
async def update_plato(
    dish: DishCreate,
    plato_id: int = Path(..., ge=1, description="ID del plato"),
    db: AsyncSession = Depends(get_db),
):
    """Modificar o actualizar un plato existente"""
    return {"msg": f"Plato {plato_id} actualizado"}

# Crear platos → POST
@router.post("/", response_model=DishOut, status_code=201)
async def create_plato(
    dish: DishCreate,
    db: AsyncSession = Depends(get_db)
):
    """Crear un nuevo plato"""
    return {"msg": "Plato creado correctamente"}

# Eliminar platos → DELETE
@router.delete("/{plato_id}", response_model=MessageOut)
async def delete_plato(
    plato_id: int = Path(..., ge=1, description="ID del plato"),
    db: AsyncSession = Depends(get_db),
):
    """Eliminar un plato"""
    return {"msg": f"Plato {plato_id} eliminado"}

# Mostrar alérgeno → GET
@router.get("/{plato_id}/alergeno", response_model=List[dict])
async def mostrar_alergeno(
    plato_id: int = Path(..., ge=1, description="ID del plato"),
    db: AsyncSession = Depends(get_db),
):
    """Obtener los alérgenos de un plato"""
    return []
