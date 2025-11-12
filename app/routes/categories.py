from fastapi import APIRouter, Depends, Path, Query, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app.database import get_db
from app.schemas.category import (
    CategoryCreate,
    CategoryUpdate,
    CategoryOut,
    CategoryListOut,
    MessageOut
)
from app.controllers.categories import (
    get_all_categories,
    get_category_by_id,
    create_category,
    update_category,
    delete_category,
    search_categories_by_name
)
from app.models.categories import Category

router = APIRouter(prefix="/categorias", tags=["Categorías"])

@router.get("/list", response_model=CategoryListOut)
async def list_categorias(db: AsyncSession = Depends(get_db)):
    """Obtener lista de todas las categorías"""
    categories = await get_all_categories(db)
    return {"items": categories}

@router.get("/{categoria_id}", response_model=CategoryOut)
async def get_categoria(
    categoria_id: int = Path(..., ge=1, description="ID de la categoría"),
    db: AsyncSession = Depends(get_db),
):
    """Obtener información de una categoría específica"""
    return await get_category_by_id(db, categoria_id)

@router.post("/", response_model=CategoryOut, status_code=status.HTTP_201_CREATED)
async def create_categoria(
    category: CategoryCreate,
    db: AsyncSession = Depends(get_db)
):
    """Crear una nueva categoría"""
    return await create_category(db, category)

@router.put("/{categoria_id}", response_model=CategoryOut)
async def modify_categoria(
    category: CategoryUpdate,
    categoria_id: int = Path(..., ge=1, description="ID de la categoría"),
    db: AsyncSession = Depends(get_db),
):
    """Modificar una categoría existente"""
    return await update_category(db, categoria_id, category)

# Nota: Tienes dos endpoints PUT muy similares. 
# Considera si realmente necesitas ambos.
@router.put("/{categoria_id}/actualizar", response_model=CategoryOut)
async def update_categoria(
    category: CategoryUpdate,
    categoria_id: int = Path(..., ge=1, description="ID de la categoría"),
    db: AsyncSession = Depends(get_db),
):
    """Actualizar una categoría existente"""
    return await update_category(db, categoria_id, category)

@router.delete("/{categoria_id}", response_model=MessageOut)
async def delete_categoria(
    categoria_id: int = Path(..., ge=1, description="ID de la categoría"),
    db: AsyncSession = Depends(get_db),
):
    """Eliminar una categoría"""
    return await delete_category(db, categoria_id)

# Endpoints adicionales

# Búsqueda de categorías por nombre
@router.get("/search/{name}", response_model=CategoryListOut)
async def search_categorias_by_name(
    name: str = Path(..., description="Nombre o parte del nombre de la categoría"),
    db: AsyncSession = Depends(get_db),
):
    """Buscar categorías por nombre"""
    categories = await search_categories_by_name(db, name)
    return {"items": categories}

# Obtener categorías con establecimientos (ejemplo de relación)
@router.get("/{categoria_id}/establecimientos", response_model=List[dict])
async def get_establecimientos_by_categoria(
    categoria_id: int = Path(..., ge=1, description="ID de la categoría"),
    db: AsyncSession = Depends(get_db),
):
    """Obtener los establecimientos de una categoría"""
    # Verificar que la categoría existe
    category = await get_category_by_id(db, categoria_id)
    
    # Aquí puedes implementar la lógica para obtener establecimientos
    # Por ahora retornamos placeholder
    return []