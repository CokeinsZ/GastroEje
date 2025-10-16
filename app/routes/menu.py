from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database import get_db
from app.schemas.menus import MenuCreate, MenuUpdate, MenuOut, MenuMessageOut
from app.schemas.dishes import DishOut

router = APIRouter(prefix="/menu", tags=["menu"])

@router.post("/{establishment_id}", response_model=MenuOut, status_code=201, summary="Crear nuevo menú")
async def create_menu_item(
    menu: MenuCreate,
    establishment_id: int = Path(..., title="ID del establecimiento"),
    db: AsyncSession = Depends(get_db)
):
    """Crear un nuevo menú para un establecimiento"""
    return {"msg": "Menú creado"}

@router.get("/{menu_id}", response_model=List[DishOut], summary="Listar todos los ítems de menú")
async def list_all_menu_items(
    menu_id: int = Path(..., title="ID del menú"),
    db: AsyncSession = Depends(get_db)
):
    """Obtener todos los platos de un menú específico"""
    return []

@router.get("/establecimiento/{establishment_id}", response_model=List[MenuOut], summary="Listar menus por establecimiento")
async def list_items_by_establishment(
    establishment_id: int = Path(..., title="ID del establecimiento"),
    db: AsyncSession = Depends(get_db)
):
    """Obtener todos los menús de un establecimiento"""
    return []

@router.get("/{menu_id}/categoria/{category_id}", response_model=List[DishOut], summary="Filtrar ítems por categoría")
async def list_items_by_category(
    menu_id: int = Path(..., title="ID del menú"),
    category_id: int = Path(..., title="ID de la categoría"),
    db: AsyncSession = Depends(get_db)
):
    """Filtrar platos de un menú por categoría"""
    return []

@router.get("/{menu_id}/item/{item_id}", response_model=DishOut, summary="Obtener detalle de un ítem de menú")
async def get_menu_item(
    menu_id: int = Path(..., title="ID del menú"),
    item_id: int = Path(..., title="ID del ítem de menú"),
    db: AsyncSession = Depends(get_db)
):
    """Obtener detalle de un plato específico del menú"""
    return {"msg": f"Detalle del ítem de menú {item_id} en el menú {menu_id}"}

# Actualizar menú
@router.put("/{menu_id}", response_model=MenuOut, summary="Actualizar menú")
async def update_menu_item(
    menu: MenuUpdate,
    menu_id: int = Path(..., title="ID del menú"),
    db: AsyncSession = Depends(get_db)
):
    """Actualizar un menú existente"""
    return {"msg": f"Menú {menu_id} actualizado"}

# Eliminar menú
@router.delete("/{menu_id}", response_model=MenuMessageOut, summary="Eliminar ítem de menú")
async def delete_menu_item(
    menu_id: int = Path(..., title="ID del ítem de menú"),
    db: AsyncSession = Depends(get_db)
):
    """Eliminar un menú"""
    return {"message": f"Ítem de menú {menu_id} eliminado"}