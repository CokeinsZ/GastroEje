from sqlalchemy import insert, update, delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from fastapi import HTTPException

from app.models.menus import Menu
from app.models.dishes import Dish
from app.models.dish_category import DishCategory
from app.schemas.menus import MenuCreate, MenuUpdate, MenuOut, MenuMessageOut
from app.schemas.dishes import DishOut


async def create_menu(menu: MenuCreate, db: AsyncSession) -> MenuOut:
    """Crear un nuevo menú para un establecimiento"""
    query = insert(Menu).values(
        title=menu.title,
        establishment_id=menu.establishment_id
    ).returning(Menu)
    
    result = await db.execute(query)
    await db.commit()
    new_menu = result.scalar_one()
    
    return MenuOut(
        menu_id=new_menu.menu_id,
        title=new_menu.title,
        establishment_id=new_menu.establishment_id
    )


async def get_menu_dishes(menu_id: int, db: AsyncSession) -> list[DishOut]:
    """Obtener todos los platos de un menú específico"""
    # Verificar que el menú existe
    menu_query = select(Menu).where(Menu.menu_id == menu_id)
    menu_result = await db.execute(menu_query)
    menu = menu_result.scalar_one_or_none()
    
    if not menu:
        raise HTTPException(status_code=404, detail="Menú no encontrado")
    
    # Obtener los platos del menú
    query = select(Dish).where(Dish.menu_id == menu_id)
    result = await db.execute(query)
    dishes = result.scalars().all()
    
    return [DishOut.model_validate(dish) for dish in dishes]


async def get_menus_by_establishment(establishment_id: int, db: AsyncSession) -> list[MenuOut]:
    """Obtener todos los menús de un establecimiento"""
    query = select(Menu).where(Menu.establishment_id == establishment_id)
    result = await db.execute(query)
    menus = result.scalars().all()
    
    return [MenuOut.model_validate(menu) for menu in menus]


async def get_menu_dishes_by_category(menu_id: int, category_id: int, db: AsyncSession) -> list[DishOut]:
    """Filtrar platos de un menú por categoría"""
    # Verificar que el menú existe
    menu_query = select(Menu).where(Menu.menu_id == menu_id)
    menu_result = await db.execute(menu_query)
    menu = menu_result.scalar_one_or_none()
    
    if not menu:
        raise HTTPException(status_code=404, detail="Menú no encontrado")
    
    # Obtener platos del menú filtrados por categoría
    query = (
        select(Dish)
        .join(DishCategory, Dish.dish_id == DishCategory.dish_id)
        .where(Dish.menu_id == menu_id)
        .where(DishCategory.category_id == category_id)
    )
    result = await db.execute(query)
    dishes = result.scalars().all()
    
    return [DishOut.model_validate(dish) for dish in dishes]


async def get_menu_dish(menu_id: int, item_id: int, db: AsyncSession) -> DishOut:
    """Obtener detalle de un plato específico del menú"""
    query = select(Dish).where(Dish.menu_id == menu_id, Dish.dish_id == item_id)
    result = await db.execute(query)
    dish = result.scalar_one_or_none()
    
    if not dish:
        raise HTTPException(status_code=404, detail="Plato no encontrado en este menú")
    
    return DishOut.model_validate(dish)


async def update_menu(menu_id: int, menu_data: MenuUpdate, db: AsyncSession) -> MenuOut:
    """Actualizar un menú existente"""
    # Verificar que el menú existe
    select_query = select(Menu).where(Menu.menu_id == menu_id)
    result = await db.execute(select_query)
    existing_menu = result.scalar_one_or_none()
    
    if not existing_menu:
        raise HTTPException(status_code=404, detail="Menú no encontrado")
    
    # Actualizar solo los campos proporcionados
    update_data = menu_data.model_dump(exclude_unset=True)
    
    if update_data:
        query = (
            update(Menu)
            .where(Menu.menu_id == menu_id)
            .values(**update_data)
            .returning(Menu)
        )
        result = await db.execute(query)
        await db.commit()
        updated_menu = result.scalar_one()
        
        return MenuOut.model_validate(updated_menu)
    
    return MenuOut.model_validate(existing_menu)


async def delete_menu(menu_id: int, db: AsyncSession) -> MenuMessageOut:
    """Eliminar un menú"""
    # Verificar que el menú existe
    select_query = select(Menu).where(Menu.menu_id == menu_id)
    result = await db.execute(select_query)
    menu = result.scalar_one_or_none()
    
    if not menu:
        raise HTTPException(status_code=404, detail="Menú no encontrado")
    
    # Eliminar el menú
    query = delete(Menu).where(Menu.menu_id == menu_id)
    await db.execute(query)
    await db.commit()
    
    return MenuMessageOut(message=f"Menú {menu_id} eliminado exitosamente")