from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db

router = APIRouter(prefix="/menu", tags=["menu"])

@router.post("/{establishment_id}", summary="Crear nuevo menú")
async def create_menu_item(
    establishment_id: int = Path(..., title="ID del establecimiento"),
    db: AsyncSession = Depends(get_db)
):
    return {"msg": "Menú creado"}

@router.get("/{menu_id}", summary="Listar todos los ítems de menú")
async def list_all_menu_items(
    menu_id: int = Path(..., title="ID del menú"),
    db: AsyncSession = Depends(get_db)
):
    return {"msg": f"Listado de todos los ítems de menú para el menú {menu_id}"}

@router.get("/establecimiento/{establishment_id}", summary="Listar menus por establecimiento")
async def list_items_by_establishment(
    establishment_id: int = Path(..., title="ID del establecimiento"),
    db: AsyncSession = Depends(get_db)
):
    return {"msg": f"Listado de menús para el establecimiento {establishment_id}"}

@router.get("/{menu_id}/categoria/{category_id}", summary="Filtrar ítems por categoría")
async def list_items_by_category(
    menu_id: int = Path(..., title="ID del menú"),
    category_id: int = Path(..., title="ID de la categoría"),
    db: AsyncSession = Depends(get_db)
):
    return {"msg": f"Listado de ítems filtrado por la categoría {category_id} en el menú {menu_id}"}

@router.get("/{menu_id}/item/{item_id}", summary="Obtener detalle de un ítem de menú")
async def get_menu_item(
    menu_id: int = Path(..., title="ID del menú"),
    item_id: int = Path(..., title="ID del ítem de menú"),
    db: AsyncSession = Depends(get_db)
):
    return {"msg": f"Detalle del ítem de menú {item_id} en el menú {menu_id}"}

# Actualizar menú
@router.put("/{menu_id}", summary="Actualizar menú")
async def update_menu_item(
    menu_id: int = Path(..., title="ID del menú"),
    db: AsyncSession = Depends(get_db)
):
    return {"msg": f"Menú {menu_id} actualizado"}

# Eliminar menú
@router.delete("/{menu_id}", summary="Eliminar ítem de menú")
async def delete_menu_item(
    menu_id: int = Path(..., title="ID del ítem de menú"),
    db: AsyncSession = Depends(get_db)
):
    return {"msg": f"Ítem de menú {menu_id} eliminado"}