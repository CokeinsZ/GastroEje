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
from app.schemas.establishment import EstablishmentOut
from app.schemas.dishes import DishOut
from app.controllers.categories import (
    get_all_categories,
    get_category_by_id,
    create_category,
    update_category,
    delete_category,
    search_categories_by_name,
    get_establishments_by_category,
    add_category_to_establishment,
    remove_category_from_establishment,
    get_dishes_by_category,
    add_category_to_dish,
    remove_category_from_dish
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
    result = await delete_category(db, categoria_id)
    return {"msg": result["message"]}

# Endpoints adicionales

# Búsqueda de categorías por nombre
@router.get("/search/{name}", response_model=CategoryListOut)
async def search_categorias(
    name: str = Path(..., description="Nombre o parte del nombre de la categoría"),
    db: AsyncSession = Depends(get_db),
):
    """Buscar categorías por nombre"""
    categories = await search_categories_by_name(db, name)
    return {"items": categories}

# Obtener establecimientos por categoría
@router.get("/{categoria_id}/establecimientos", response_model=List[EstablishmentOut])
async def get_establecimientos_by_categoria(
    categoria_id: int = Path(..., ge=1, description="ID de la categoría"),
    db: AsyncSession = Depends(get_db),
):
    """Obtener los establecimientos de una categoría"""
    return await get_establishments_by_category(db, categoria_id)


# Agregar categoría a establecimiento
@router.post("/establecimiento/{establishment_id}/categoria/{categoria_id}", response_model=MessageOut)
async def add_categoria_to_establishment(
    establishment_id: int = Path(..., ge=1, description="ID del establecimiento"),
    categoria_id: int = Path(..., ge=1, description="ID de la categoría"),
    db: AsyncSession = Depends(get_db),
):
    """Asociar una categoría a un establecimiento"""
    await add_category_to_establishment(db, establishment_id, categoria_id)
    return {"msg": "Categoría asociada al establecimiento correctamente"}


# Eliminar categoría de establecimiento
@router.delete("/establecimiento/{establishment_id}/categoria/{categoria_id}", response_model=MessageOut)
async def remove_categoria_from_establishment(
    establishment_id: int = Path(..., ge=1, description="ID del establecimiento"),
    categoria_id: int = Path(..., ge=1, description="ID de la categoría"),
    db: AsyncSession = Depends(get_db),
):
    """Eliminar la asociación de una categoría con un establecimiento"""
    await remove_category_from_establishment(db, establishment_id, categoria_id)
    return {"msg": "Categoría eliminada del establecimiento correctamente"}


# Obtener platos por categoría
@router.get("/{categoria_id}/platos", response_model=List[DishOut])
async def get_platos_by_categoria(
    categoria_id: int = Path(..., ge=1, description="ID de la categoría"),
    db: AsyncSession = Depends(get_db),
):
    """Obtener los platos de una categoría"""
    return await get_dishes_by_category(db, categoria_id)


# Agregar categoría a plato
@router.post("/plato/{dish_id}/categoria/{categoria_id}", response_model=MessageOut)
async def add_categoria_to_dish(
    dish_id: int = Path(..., ge=1, description="ID del plato"),
    categoria_id: int = Path(..., ge=1, description="ID de la categoría"),
    db: AsyncSession = Depends(get_db),
):
    """Asociar una categoría a un plato"""
    await add_category_to_dish(db, dish_id, categoria_id)
    return {"msg": "Categoría asociada al plato correctamente"}


# Eliminar categoría de plato
@router.delete("/plato/{dish_id}/categoria/{categoria_id}", response_model=MessageOut)
async def remove_categoria_from_dish(
    dish_id: int = Path(..., ge=1, description="ID del plato"),
    categoria_id: int = Path(..., ge=1, description="ID de la categoría"),
    db: AsyncSession = Depends(get_db),
):
    """Eliminar la asociación de una categoría con un plato"""
    await remove_category_from_dish(db, dish_id, categoria_id)
    return {"msg": "Categoría eliminada del plato correctamente"}
