from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.category import (
    CategoryCreate,
    CategoryUpdate,
    CategoryOut,
    CategoryListOut,
    MessageOut
)

router = APIRouter(prefix="/categorias", tags=["Categorías"])

@router.get("/list", response_model=CategoryListOut)
async def list_categorias(db: AsyncSession = Depends(get_db)):
    """Obtener lista de todas las categorías"""
    return {"items": []}

@router.get("/{categoria_id}", response_model=CategoryOut)
async def get_categoria(
    categoria_id: int = Path(..., ge=1, description="ID de la categoría"),
    db: AsyncSession = Depends(get_db),
):
    """Obtener información de una categoría específica"""
    return {"msg": f"Información de la categoría {categoria_id}"}

@router.post("/", response_model=CategoryOut, status_code=201)
async def create_categoria(
    category: CategoryCreate,
    db: AsyncSession = Depends(get_db)
):
    """Crear una nueva categoría"""
    return {"msg": "Categoría creada correctamente"}

@router.put("/{categoria_id}", response_model=CategoryOut)
async def modify_categoria(
    category: CategoryUpdate,
    categoria_id: int = Path(..., ge=1, description="ID de la categoría"),
    db: AsyncSession = Depends(get_db),
):
    """Modificar una categoría existente"""
    return {"msg": f"Categoría {categoria_id} modificada"}

@router.put("/{categoria_id}/actualizar", response_model=CategoryOut)
async def update_categoria(
    category: CategoryUpdate,
    categoria_id: int = Path(..., ge=1, description="ID de la categoría"),
    db: AsyncSession = Depends(get_db),
):
    """Actualizar una categoría existente"""
    return {"msg": f"Categoría {categoria_id} actualizada"}

@router.delete("/{categoria_id}", response_model=MessageOut)
async def delete_categoria(
    categoria_id: int = Path(..., ge=1, description="ID de la categoría"),
    db: AsyncSession = Depends(get_db),
):
    """Eliminar una categoría"""
    return {"msg": f"Categoría {categoria_id} eliminada"}
