from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from fastapi import HTTPException, status
from app.models.categories import Category
from app.models.establishment_category import EstablishmentCategory
from app.models.dish_category import DishCategory
from app.models.establishments import Establishment
from app.models.dishes import Dish
from app.schemas.category import CategoryCreate, CategoryUpdate

# Obtener todas las categorías
async def get_all_categories(db: AsyncSession):
    """Obtener lista de todas las categorías"""
    try:
        query = select(Category)
        result = await db.execute(query)
        categories = result.scalars().all()
        return categories
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener categorías: {str(e)}"
        )

# Obtener una categoría por ID
async def get_category_by_id(db: AsyncSession, category_id: int):
    """Obtener una categoría específica por su ID"""
    try:
        query = select(Category).where(Category.category_id == category_id)
        result = await db.execute(query)
        category = result.scalar_one_or_none()

        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Categoría con ID {category_id} no encontrada"
            )
        return category
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener categoría: {str(e)}"
        )

# Crear una nueva categoría
async def create_category(db: AsyncSession, category_data: CategoryCreate):
    """Crear una nueva categoría en la base de datos"""
    try:
        # Verificar si ya existe una categoría con el mismo nombre
        query = select(Category).where(Category.name == category_data.name)
        result = await db.execute(query)
        existing_category = result.scalar_one_or_none()

        if existing_category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe una categoría con ese nombre"
            )

        new_category = Category(
            name=category_data.name,
            description=category_data.description
        )
        
        db.add(new_category)
        await db.commit()
        await db.refresh(new_category)
        return new_category
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear categoría: {str(e)}"
        )

# Actualizar una categoría existente
async def update_category(db: AsyncSession, category_id: int, category_data: CategoryUpdate):
    """Actualizar una categoría existente"""
    try:
        # Verificar si la categoría existe
        query_exists = select(Category).where(Category.category_id == category_id)
        result_exists = await db.execute(query_exists)
        existing_category = result_exists.scalar_one_or_none()
        
        if not existing_category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Categoría con ID {category_id} no encontrada"
            )

        # Si se está actualizando el nombre, verificar que no exista otro con el mismo nombre
        if category_data.name is not None:
            query_name = select(Category).where(
                Category.name == category_data.name,
                Category.category_id != category_id
            )
            result_name = await db.execute(query_name)
            duplicate_category = result_name.scalar_one_or_none()
            if duplicate_category:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Ya existe otra categoría con ese nombre"
                )

        # Preparar datos para actualizar
        update_data = {}
        if category_data.name is not None:
            update_data['name'] = category_data.name
        if category_data.description is not None:
            update_data['description'] = category_data.description

        # Ejecutar actualización
        query = (
            update(Category)
            .where(Category.category_id == category_id)
            .values(**update_data)
            .execution_options(synchronize_session="fetch")
        )
        await db.execute(query)
        await db.commit()

        # Obtener la categoría actualizada
        query_updated = select(Category).where(Category.category_id == category_id)
        result_updated = await db.execute(query_updated)
        updated_category = result_updated.scalar_one()
        
        return updated_category
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar categoría: {str(e)}"
        )

# Eliminar una categoría
async def delete_category(db: AsyncSession, category_id: int):
    """Eliminar una categoría de la base de datos"""
    try:
        # Verificar si la categoría existe
        query_exists = select(Category).where(Category.category_id == category_id)
        result_exists = await db.execute(query_exists)
        existing_category = result_exists.scalar_one_or_none()
        
        if not existing_category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Categoría con ID {category_id} no encontrada"
            )

        # Eliminar la categoría
        query = delete(Category).where(Category.category_id == category_id)
        await db.execute(query)
        await db.commit()

        return {"message": f"Categoría con ID {category_id} eliminada correctamente"}
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar categoría: {str(e)}"
        )

# Búsqueda de categorías por nombre
async def search_categories_by_name(db: AsyncSession, name: str):
    """Buscar categorías por nombre"""
    try:
        query = select(Category).where(Category.name.ilike(f"%{name}%"))
        result = await db.execute(query)
        categories = result.scalars().all()
        return categories
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error en la búsqueda: {str(e)}"
        )


# Obtener establecimientos por categoría
async def get_establishments_by_category(db: AsyncSession, category_id: int):
    """Obtener todos los establecimientos de una categoría"""
    try:
        # Verificar que la categoría existe
        category_query = select(Category).where(Category.category_id == category_id)
        category_result = await db.execute(category_query)
        category = category_result.scalar_one_or_none()
        
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Categoría con ID {category_id} no encontrada"
            )
        
        # Obtener los establecimientos
        query = (
            select(Establishment)
            .join(EstablishmentCategory)
            .where(EstablishmentCategory.category_id == category_id)
        )
        result = await db.execute(query)
        establishments = result.scalars().all()
        return establishments
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener establecimientos: {str(e)}"
        )


# Agregar categoría a establecimiento
async def add_category_to_establishment(db: AsyncSession, establishment_id: int, category_id: int):
    """Asociar una categoría a un establecimiento"""
    try:
        # Verificar que el establecimiento existe
        est_query = select(Establishment).where(Establishment.establishment_id == establishment_id)
        est_result = await db.execute(est_query)
        establishment = est_result.scalar_one_or_none()
        
        if not establishment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Establecimiento con ID {establishment_id} no encontrado"
            )
        
        # Verificar que la categoría existe
        cat_query = select(Category).where(Category.category_id == category_id)
        cat_result = await db.execute(cat_query)
        category = cat_result.scalar_one_or_none()
        
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Categoría con ID {category_id} no encontrada"
            )
        
        # Verificar si ya existe la asociación
        existing_query = select(EstablishmentCategory).where(
            EstablishmentCategory.establishment_id == establishment_id,
            EstablishmentCategory.category_id == category_id
        )
        existing_result = await db.execute(existing_query)
        existing = existing_result.scalar_one_or_none()
        
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La categoría ya está asociada a este establecimiento"
            )
        
        # Crear la asociación
        est_cat = EstablishmentCategory(establishment_id=establishment_id, category_id=category_id)
        db.add(est_cat)
        await db.commit()
        return True
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al asociar categoría: {str(e)}"
        )


# Eliminar categoría de establecimiento
async def remove_category_from_establishment(db: AsyncSession, establishment_id: int, category_id: int):
    """Eliminar la asociación de una categoría con un establecimiento"""
    try:
        result = await db.execute(
            select(EstablishmentCategory)
            .where(EstablishmentCategory.establishment_id == establishment_id)
            .where(EstablishmentCategory.category_id == category_id)
        )
        est_cat = result.scalar_one_or_none()
        
        if not est_cat:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Asociación no encontrada"
            )
        
        await db.delete(est_cat)
        await db.commit()
        return True
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar asociación: {str(e)}"
        )


# Obtener platos por categoría
async def get_dishes_by_category(db: AsyncSession, category_id: int):
    """Obtener todos los platos de una categoría"""
    try:
        # Verificar que la categoría existe
        category_query = select(Category).where(Category.category_id == category_id)
        category_result = await db.execute(category_query)
        category = category_result.scalar_one_or_none()
        
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Categoría con ID {category_id} no encontrada"
            )
        
        # Obtener los platos
        query = (
            select(Dish)
            .join(DishCategory)
            .where(DishCategory.category_id == category_id)
        )
        result = await db.execute(query)
        dishes = result.scalars().all()
        return dishes
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener platos: {str(e)}"
        )


# Agregar categoría a plato
async def add_category_to_dish(db: AsyncSession, dish_id: int, category_id: int):
    """Asociar una categoría a un plato"""
    try:
        # Verificar que el plato existe
        dish_query = select(Dish).where(Dish.dish_id == dish_id)
        dish_result = await db.execute(dish_query)
        dish = dish_result.scalar_one_or_none()
        
        if not dish:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Plato con ID {dish_id} no encontrado"
            )
        
        # Verificar que la categoría existe
        cat_query = select(Category).where(Category.category_id == category_id)
        cat_result = await db.execute(cat_query)
        category = cat_result.scalar_one_or_none()
        
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Categoría con ID {category_id} no encontrada"
            )
        
        # Verificar si ya existe la asociación
        existing_query = select(DishCategory).where(
            DishCategory.dish_id == dish_id,
            DishCategory.category_id == category_id
        )
        existing_result = await db.execute(existing_query)
        existing = existing_result.scalar_one_or_none()
        
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La categoría ya está asociada a este plato"
            )
        
        # Crear la asociación
        dish_cat = DishCategory(dish_id=dish_id, category_id=category_id)
        db.add(dish_cat)
        await db.commit()
        return True
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al asociar categoría: {str(e)}"
        )


# Eliminar categoría de plato
async def remove_category_from_dish(db: AsyncSession, dish_id: int, category_id: int):
    """Eliminar la asociación de una categoría con un plato"""
    try:
        result = await db.execute(
            select(DishCategory)
            .where(DishCategory.dish_id == dish_id)
            .where(DishCategory.category_id == category_id)
        )
        dish_cat = result.scalar_one_or_none()
        
        if not dish_cat:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Asociación no encontrada"
            )
        
        await db.delete(dish_cat)
        await db.commit()
        return True
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar asociación: {str(e)}"
        )
