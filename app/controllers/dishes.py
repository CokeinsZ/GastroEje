from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from fastapi import HTTPException, status
from app.models.dishes import Dish
from app.schemas.dishes import DishCreate, DishUpdate

# Obtener todos los platos
async def get_all_dishes(db: AsyncSession):
    """Obtener lista de todos los platos"""
    try:
        query = select(Dish)
        result = await db.execute(query)
        dishes = result.scalars().all()
        return dishes
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener platos: {str(e)}"
        )

# Obtener un plato por ID
async def get_dish_by_id(db: AsyncSession, dish_id: int):
    """Obtener un plato específico por su ID"""
    try:
        query = select(Dish).where(Dish.dish_id == dish_id)
        result = await db.execute(query)
        dish = result.scalar_one_or_none()

        if not dish:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Plato con ID {dish_id} no encontrado"
            )
        return dish
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener plato: {str(e)}"
        )

# Crear un nuevo plato
async def create_dish(db: AsyncSession, dish_data: DishCreate):
    """Crear un nuevo plato en la base de datos"""
    try:
        # Validar que el precio sea positivo
        if dish_data.price <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El precio debe ser mayor a 0"
            )

        new_dish = Dish(
            menu_id=dish_data.menu_id,
            name=dish_data.name,
            description=dish_data.description,
            price=dish_data.price,
            img=dish_data.img
        )
        
        db.add(new_dish)
        await db.commit()
        await db.refresh(new_dish)
        return new_dish
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear plato: {str(e)}"
        )

# Actualizar un plato existente
async def update_dish(db: AsyncSession, dish_id: int, dish_data: DishUpdate):
    """Actualizar un plato existente"""
    try:
        # Verificar si el plato existe
        query_exists = select(Dish).where(Dish.dish_id == dish_id)
        result_exists = await db.execute(query_exists)
        existing_dish = result_exists.scalar_one_or_none()
        
        if not existing_dish:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Plato con ID {dish_id} no encontrado"
            )

        # Validar precio si se está actualizando
        if dish_data.price is not None and dish_data.price <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El precio debe ser mayor a 0"
            )

        # Preparar datos para actualizar (excluir valores no proporcionados)
        update_data = {}
        if dish_data.menu_id is not None:
            update_data['menu_id'] = dish_data.menu_id
        if dish_data.name is not None:
            update_data['name'] = dish_data.name
        if dish_data.description is not None:
            update_data['description'] = dish_data.description
        if dish_data.price is not None:
            update_data['price'] = dish_data.price
        if dish_data.img is not None:
            update_data['img'] = dish_data.img

        # Ejecutar actualización
        query = (
            update(Dish)
            .where(Dish.dish_id == dish_id)
            .values(**update_data)
            .execution_options(synchronize_session="fetch")
        )
        await db.execute(query)
        await db.commit()

        # Obtener el plato actualizado
        query_updated = select(Dish).where(Dish.dish_id == dish_id)
        result_updated = await db.execute(query_updated)
        updated_dish = result_updated.scalar_one()
        
        return updated_dish
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar plato: {str(e)}"
        )

# Eliminar un plato
async def delete_dish(db: AsyncSession, dish_id: int):
    """Eliminar un plato de la base de datos"""
    try:
        # Verificar si el plato existe
        query_exists = select(Dish).where(Dish.dish_id == dish_id)
        result_exists = await db.execute(query_exists)
        existing_dish = result_exists.scalar_one_or_none()
        
        if not existing_dish:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Plato con ID {dish_id} no encontrado"
            )

        # Eliminar el plato
        query = delete(Dish).where(Dish.dish_id == dish_id)
        await db.execute(query)
        await db.commit()

        return {"message": f"Plato con ID {dish_id} eliminado correctamente"}
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar plato: {str(e)}"
        )

# Obtener platos por menú
async def get_dishes_by_menu(db: AsyncSession, menu_id: int):
    """Obtener todos los platos de un menú específico"""
    try:
        query = select(Dish).where(Dish.menu_id == menu_id)
        result = await db.execute(query)
        dishes = result.scalars().all()
        return dishes
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener platos del menú: {str(e)}"
        )

# Obtener platos con precio mayor a (ejemplo con filtro)
async def get_dishes_price_gt(db: AsyncSession, min_price: float):
    """Obtener platos con precio mayor al especificado"""
    try:
        query = select(Dish).where(Dish.price > min_price)
        result = await db.execute(query)
        dishes = result.scalars().all()
        return dishes
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener platos: {str(e)}"
        )