from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from app.models.allergens import Allergens
from app.models.user_allergen import UserAllergen
from app.models.dish_allergen import DishAllergen
from app.schemas.allergens import AllergenCreate, AllergenUpdate


async def create_allergen(db: AsyncSession, data: AllergenCreate):
    """Crear un nuevo alérgeno"""
    allergen = Allergens(**data.model_dump())
    db.add(allergen)
    await db.commit()
    await db.refresh(allergen)
    return allergen


async def get_allergens(db: AsyncSession):
    """Obtener todos los alérgenos"""
    result = await db.execute(select(Allergens))
    return result.scalars().all()


async def get_allergen_by_id(db: AsyncSession, allergen_id: int):
    """Obtener un alérgeno por ID"""
    result = await db.execute(
        select(Allergens).where(Allergens.allergen_id == allergen_id)
    )
    allergen = result.scalar_one_or_none()
    if not allergen:
        raise HTTPException(status_code=404, detail="Allergen not found")
    return allergen


async def get_allergens_by_dish(db: AsyncSession, dish_id: int):
    """Obtener todos los alérgenos de un plato"""
    result = await db.execute(
        select(Allergens)
        .join(DishAllergen)
        .where(DishAllergen.dish_id == dish_id)
    )
    return result.scalars().all()


async def get_allergens_by_user(db: AsyncSession, user_id: int):
    """Obtener todos los alérgenos de un usuario"""
    result = await db.execute(
        select(Allergens)
        .join(UserAllergen)
        .where(UserAllergen.user_id == user_id)
    )
    return result.scalars().all()


async def add_allergen_to_user(db: AsyncSession, user_id: int, allergen_id: int):
    """Asociar un alérgeno a un usuario"""
    user_allergen = UserAllergen(user_id=user_id, allergen_id=allergen_id)
    db.add(user_allergen)
    await db.commit()
    return True


async def remove_allergen_from_user(db: AsyncSession, user_id: int, allergen_id: int):
    """Eliminar la asociación de un alérgeno con un usuario"""
    result = await db.execute(
        select(UserAllergen)
        .where(UserAllergen.user_id == user_id)
        .where(UserAllergen.allergen_id == allergen_id)
    )
    user_allergen = result.scalar_one_or_none()
    if not user_allergen:
        raise HTTPException(status_code=404, detail="Association not found")
    
    await db.delete(user_allergen)
    await db.commit()
    return True


async def update_allergen(db: AsyncSession, allergen_id: int, data: AllergenUpdate):
    """Actualizar un alérgeno"""
    result = await db.execute(
        select(Allergens).where(Allergens.allergen_id == allergen_id)
    )
    allergen = result.scalar_one_or_none()
    if not allergen:
        raise HTTPException(status_code=404, detail="Allergen not found")
    
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(allergen, key, value)
    
    await db.commit()
    await db.refresh(allergen)
    return allergen


async def delete_allergen(db: AsyncSession, allergen_id: int):
    """Eliminar un alérgeno"""
    result = await db.execute(
        select(Allergens).where(Allergens.allergen_id == allergen_id)
    )
    allergen = result.scalar_one_or_none()
    if not allergen:
        raise HTTPException(status_code=404, detail="Allergen not found")
    
    await db.delete(allergen)
    await db.commit()
    return True
