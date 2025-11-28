from fastapi import APIRouter, Depends, Path, Query, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from typing import List, Optional

from app.database import get_db
from app.schemas.dishes import DishCreate, DishOut, DishUpdate
from app.schemas.category import MessageOut
from app.schemas.allergens import AllergenOut
from app.controllers.dishes import (
    get_all_dishes, 
    get_dish_by_id, 
    create_dish, 
    update_dish, 
    delete_dish,
    get_dishes_by_menu,
    get_dishes_price_gt,
    get_allergens_by_dish,
    add_allergen_to_dish,
    remove_allergen_from_dish
)
from app.models.dishes import Dish 

router = APIRouter(prefix="/platos", tags=["Platos"])

# Listar platos → GET
@router.get("/list", response_model=List[DishOut])
async def list_platos(db: AsyncSession = Depends(get_db)):
    """Obtener lista de todos los platos"""
    return await get_all_dishes(db)

# Mostrar info de un plato → GET
@router.get("/{plato_id}", response_model=DishOut)
async def get_plato(
    plato_id: int = Path(..., ge=1, description="ID del plato"),
    db: AsyncSession = Depends(get_db),
):
    """Obtener información de un plato específico"""
    return await get_dish_by_id(db, plato_id)

# Crear platos → POST
@router.post("/", response_model=DishOut, status_code=status.HTTP_201_CREATED)
async def create_plato(
    dish: DishCreate,
    db: AsyncSession = Depends(get_db)
):
    """Crear un nuevo plato"""
    return await create_dish(db, dish)

# Modificar o actualizar plato → PUT
@router.put("/{plato_id}", response_model=DishOut)
async def update_plato(
    dish: DishUpdate,
    plato_id: int = Path(..., ge=1, description="ID del plato"),
    db: AsyncSession = Depends(get_db),
):
    """Modificar o actualizar un plato existente"""
    return await update_dish(db, plato_id, dish)

# Eliminar platos → DELETE
@router.delete("/{plato_id}", response_model=MessageOut)
async def delete_plato(
    plato_id: int = Path(..., ge=1, description="ID del plato"),
    db: AsyncSession = Depends(get_db),
):
    """Eliminar un plato"""
    return await delete_dish(db, plato_id)

# Endpoints adicionales siguiendo el estilo del profesor

# Listar platos por menú → GET
@router.get("/menu/{menu_id}", response_model=List[DishOut])
async def list_platos_by_menu(
    menu_id: int = Path(..., ge=1, description="ID del menú"),
    db: AsyncSession = Depends(get_db),
):
    """Obtener todos los platos de un menú específico"""
    return await get_dishes_by_menu(db, menu_id)

# Listar platos con precio mayor a → GET
@router.get("/filter/price", response_model=List[DishOut])
async def list_platos_price_gt(
    min_price: float = Query(..., ge=0, description="Precio mínimo"),
    db: AsyncSession = Depends(get_db),
):
    """Obtener platos con precio mayor al especificado"""
    return await get_dishes_price_gt(db, min_price)

# Mostrar alérgenos → GET
@router.get("/{plato_id}/alergenos", response_model=List[AllergenOut])
async def mostrar_alergenos(
    plato_id: int = Path(..., ge=1, description="ID del plato"),
    db: AsyncSession = Depends(get_db),
):
    """Obtener los alérgenos de un plato"""
    return await get_allergens_by_dish(db, plato_id)


# Agregar alérgeno a un plato → POST
@router.post("/{plato_id}/alergenos/{allergen_id}", response_model=MessageOut)
async def agregar_alergeno(
    plato_id: int = Path(..., ge=1, description="ID del plato"),
    allergen_id: int = Path(..., ge=1, description="ID del alérgeno"),
    db: AsyncSession = Depends(get_db),
):
    """Asociar un alérgeno a un plato"""
    await add_allergen_to_dish(db, plato_id, allergen_id)
    return {"msg": "Alérgeno asociado al plato correctamente"}


# Eliminar alérgeno de un plato → DELETE
@router.delete("/{plato_id}/alergenos/{allergen_id}", response_model=MessageOut)
async def eliminar_alergeno(
    plato_id: int = Path(..., ge=1, description="ID del alérgeno"),
    allergen_id: int = Path(..., ge=1, description="ID del alérgeno"),
    db: AsyncSession = Depends(get_db),
):
    """Eliminar la asociación de un alérgeno con un plato"""
    await remove_allergen_from_dish(db, plato_id, allergen_id)
    return {"msg": "Alérgeno eliminado del plato correctamente"}


# Obtener platos por nombre (búsqueda) → GET
@router.get("/search/{name}", response_model=List[DishOut])
async def search_platos_by_name(
    name: str = Path(..., description="Nombre o parte del nombre del plato"),
    db: AsyncSession = Depends(get_db),
):
    """Buscar platos por nombre"""
    try:
        query = select(Dish).where(func.lower(Dish.name).contains(func.lower(name)))
        result = await db.execute(query)
        dishes = result.scalars().all()
        return dishes
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error en la búsqueda: {str(e)}"
        )