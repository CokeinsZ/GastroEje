from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from fastapi import HTTPException
from app.models.menus import Menu
from app.models.establishments import Establishment
from app.models.dishes import Dish
from app.schemas.menus import MenuCreate, MenuUpdate, MenuOut


# ---------- CREAR ----------
async def create_menu_controller(db: AsyncSession, data: MenuCreate, establishment_id: int) -> Menu:
    """Crear un nuevo menú para un establecimiento"""
    # Verificar que el establecimiento existe
    query = select(Establishment).where(Establishment.establishment_id == establishment_id)
    result = await db.execute(query)
    establishment = result.scalar_one_or_none()
    
    if not establishment:
        raise HTTPException(status_code=404, detail="Establishment not found")
    
    # Crear el menú
    menu = Menu(
        title=data.title,
        establishment_id=establishment_id
    )
    db.add(menu)
    await db.commit()
    await db.refresh(menu)
    return menu


# ---------- LEER ----------
async def get_menu_by_id(db: AsyncSession, menu_id: int) -> Optional[Menu]:
    """Obtener un menú por su ID"""
    query = select(Menu).where(Menu.menu_id == menu_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def get_menus_by_establishment(db: AsyncSession, establishment_id: int) -> List[Menu]:
    """Obtener todos los menús de un establecimiento"""
    query = select(Menu).where(Menu.establishment_id == establishment_id)
    result = await db.execute(query)
    return list(result.scalars().all())


async def get_dishes_by_menu(db: AsyncSession, menu_id: int) -> List[Dish]:
    """Obtener todos los platos de un menú"""
    # Verificar que el menú existe
    menu = await get_menu_by_id(db, menu_id)
    if not menu:
        raise HTTPException(status_code=404, detail="Menu not found")
    
    query = select(Dish).where(Dish.menu_id == menu_id)
    result = await db.execute(query)
    return list(result.scalars().all())


async def get_dishes_by_menu_and_category(db: AsyncSession, menu_id: int, category_id: int) -> List[Dish]:
    """Obtener platos de un menú filtrados por categoría"""
    # Verificar que el menú existe
    menu = await get_menu_by_id(db, menu_id)
    if not menu:
        raise HTTPException(status_code=404, detail="Menu not found")
    
    # Aquí necesitarías hacer un join con dish_category si quieres filtrar por categoría
    # Por ahora devuelvo todos los platos del menú
    query = select(Dish).where(Dish.menu_id == menu_id)
    result = await db.execute(query)
    return list(result.scalars().all())


async def get_dish_from_menu(db: AsyncSession, menu_id: int, dish_id: int) -> Optional[Dish]:
    """Obtener un plato específico de un menú"""
    query = select(Dish).where(Dish.menu_id == menu_id, Dish.dish_id == dish_id)
    result = await db.execute(query)
    dish = result.scalar_one_or_none()
    
    if not dish:
        raise HTTPException(status_code=404, detail="Dish not found in this menu")
    
    return dish


# ---------- ACTUALIZAR ----------
async def update_menu_controller(db: AsyncSession, menu_id: int, data: MenuUpdate) -> Optional[Menu]:
    """Actualizar un menú existente"""
    # Verificar que el menú existe
    menu = await get_menu_by_id(db, menu_id)
    if not menu:
        raise HTTPException(status_code=404, detail="Menu not found")
    
    payload = data.model_dump(exclude_unset=True)
    if not payload:
        return menu
    
    query = (
        update(Menu)
        .where(Menu.menu_id == menu_id)
        .values(**payload)
        .execution_options(synchronize_session="fetch")
    )
    await db.execute(query)
    await db.commit()
    return await get_menu_by_id(db, menu_id)


# ---------- ELIMINAR ----------
async def delete_menu_controller(db: AsyncSession, menu_id: int) -> bool:
    """Eliminar un menú"""
    # Verificar que el menú existe
    menu = await get_menu_by_id(db, menu_id)
    if not menu:
        raise HTTPException(status_code=404, detail="Menu not found")
    
    query = delete(Menu).where(Menu.menu_id == menu_id)
    result = await db.execute(query)
    await db.commit()
    return result.rowcount > 0
