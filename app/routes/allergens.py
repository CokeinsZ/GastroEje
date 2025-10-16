from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database import get_db
from app.schemas.allergens import AllergenCreate, AllergenUpdate, AllergenOut, AllergenMessageOut

router = APIRouter(prefix="/allergen", tags=["allergen"])

@router.post("/", response_model=AllergenOut, status_code=201, summary="Crear nuevo alérgeno")
async def create_allergen(
    allergen: AllergenCreate,
    db: AsyncSession = Depends(get_db)
):
    """Crear un nuevo alérgeno"""
    return {"msg": "Alérgeno creado"}

@router.get("/", response_model=List[AllergenOut], summary="Listar todos los alérgenos")
async def list_allergens(
    db: AsyncSession = Depends(get_db)
):
    """Obtener lista de todos los alérgenos"""
    return []

@router.get("/{allergen_id}", response_model=AllergenOut, summary="Obtener alérgeno por ID")
async def get_allergen(
    allergen_id: int = Path(..., title="ID del alérgeno"),
    db: AsyncSession = Depends(get_db)
):
    """Obtener un alérgeno específico por su ID"""
    return {"msg": f"Alérgeno con ID {allergen_id}"}

@router.get("/dish/{dish_id}", response_model=List[AllergenOut], summary="Obtener alérgenos de un plato")
async def get_dish_allergen(
    dish_id: int = Path(..., title="ID del plato"),
    db: AsyncSession = Depends(get_db)
):
    """Obtener todos los alérgenos de un plato específico"""
    return []

@router.get("/user/{user_id}", response_model=List[AllergenOut], summary="Obtener alérgenos de un usuario")
async def get_user_allergen(
    user_id: int = Path(..., title="ID del usuario"),
    db: AsyncSession = Depends(get_db)
):
    """Obtener todos los alérgenos asociados a un usuario"""
    return []

@router.put("/{allergen_id}", response_model=AllergenOut, summary="Actualizar alérgeno")
async def update_allergen(
    allergen: AllergenUpdate,
    allergen_id: int = Path(..., title="ID del alérgeno"),
    db: AsyncSession = Depends(get_db)
):
    """Actualizar un alérgeno existente"""
    return {"msg": f"Alérgeno con ID {allergen_id} actualizado"}

@router.delete("/{allergen_id}", response_model=AllergenMessageOut, summary="Eliminar alérgeno")
async def delete_allergen(
    allergen_id: int = Path(..., title="ID del alérgeno"),
    db: AsyncSession = Depends(get_db)
):
    """Eliminar un alérgeno"""
    return {"message": f"Alérgeno con ID {allergen_id} eliminado"}