from fastapi import APIRouter, Depends, Path, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database import get_db
from app.schemas.allergens import AllergenCreate, AllergenUpdate, AllergenOut, AllergenMessageOut
from app.controllers.allergens import *

router = APIRouter(prefix="/allergen", tags=["allergen"])

@router.post("/", response_model=AllergenOut, status_code=201, summary="Crear nuevo alérgeno")
async def create_allergen_route(
    allergen: AllergenCreate,
    db: AsyncSession = Depends(get_db)
):
    """Crear un nuevo alérgeno"""
    return await create_allergen(db, allergen)

@router.get("/", response_model=List[AllergenOut], summary="Listar todos los alérgenos")
async def list_allergens(
    db: AsyncSession = Depends(get_db)
):
    """Obtener lista de todos los alérgenos"""
    return await get_allergens(db)

@router.get("/{allergen_id}", response_model=AllergenOut, summary="Obtener alérgeno por ID")
async def get_allergen(
    allergen_id: int = Path(..., title="ID del alérgeno"),
    db: AsyncSession = Depends(get_db)
):
    """Obtener un alérgeno específico por su ID"""
    allergen = await get_allergen_by_id(db, allergen_id)
    if not allergen:
        raise HTTPException(status_code=404, detail="Allergen not found")
    return allergen

@router.get("/dish/{dish_id}", response_model=List[AllergenOut], summary="Obtener alérgenos de un plato")
async def get_dish_allergen(
    dish_id: int = Path(..., title="ID del plato"),
    db: AsyncSession = Depends(get_db)
):
    """Obtener todos los alérgenos de un plato específico"""
    return await get_allergens_by_dish(db, dish_id)

@router.get("/user/{user_id}", response_model=List[AllergenOut], summary="Obtener alérgenos de un usuario")
async def get_user_allergen(
    user_id: int = Path(..., title="ID del usuario"),
    db: AsyncSession = Depends(get_db)
):
    """Obtener todos los alérgenos asociados a un usuario"""
    return await get_allergens_by_user(db, user_id)

@router.put("/{allergen_id}", response_model=AllergenOut, summary="Actualizar alérgeno")
async def update_allergen_route(
    allergen: AllergenUpdate,
    allergen_id: int = Path(..., title="ID del alérgeno"),
    db: AsyncSession = Depends(get_db)
):
    """Actualizar un alérgeno existente"""
    updated = await update_allergen(db, allergen_id, allergen)
    if not updated:
        raise HTTPException(status_code=404, detail="Allergen not found")
    return updated

@router.delete("/{allergen_id}", response_model=AllergenMessageOut, summary="Eliminar alérgeno")
async def delete_allergen_route(
    allergen_id: int = Path(..., title="ID del alérgeno"),
    db: AsyncSession = Depends(get_db)
):
    """Eliminar un alérgeno"""
    deleted = await delete_allergen(db, allergen_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Allergen not found")
    return {"message": f"Alérgeno con ID {allergen_id} eliminado"}


@router.post("/user/{user_id}/allergen/{allergen_id}", response_model=AllergenMessageOut, summary="Asociar alérgeno a usuario")
async def add_user_allergen(
    user_id: int = Path(..., title="ID del usuario"),
    allergen_id: int = Path(..., title="ID del alérgeno"),
    db: AsyncSession = Depends(get_db)
):
    """Asociar un alérgeno a un usuario"""
    await add_allergen_to_user(db, user_id, allergen_id)
    return {"message": "Alérgeno asociado al usuario"}


@router.delete("/user/{user_id}/allergen/{allergen_id}", response_model=AllergenMessageOut, summary="Desasociar alérgeno de usuario")
async def remove_user_allergen(
    user_id: int = Path(..., title="ID del usuario"),
    allergen_id: int = Path(..., title="ID del alérgeno"),
    db: AsyncSession = Depends(get_db)
):
    """Eliminar la asociación de un alérgeno con un usuario"""
    deleted = await remove_allergen_from_user(db, user_id, allergen_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Association not found")
    return {"message": "Alérgeno desasociado del usuario"}