from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db

router = APIRouter(prefix="/allergen", tags=["allergen"])

@router.post("/", summary="Crear nuevo alérgeno")
async def create_allergen(
    db: AsyncSession = Depends(get_db)
):
    return {"msg": "Alérgeno creado"}

@router.get("/", summary="Listar todos los alérgenos")
async def list_allergens(
    db: AsyncSession = Depends(get_db)
):
    return {"msg": "Lista de alérgenos"}

@router.get("/{allergen_id}", summary="Obtener alérgeno por ID")
async def get_allergen(
    allergen_id: int = Path(..., title="ID del alérgeno"),
    db: AsyncSession = Depends(get_db)
):
    return {"msg": f"Alérgeno con ID {allergen_id}"}

@router.get("/dish/{dish_id}", summary="Obtener alérgeno por ID de plato")
async def get_dish_allergen(
    dish_id: int = Path(..., title="ID del plato"),
    db: AsyncSession = Depends(get_db)
):
    return {"msg": f"Alérgeno del plato con ID {dish_id}"}

@router.get("/user/{user_id}", summary="Obtener alérgeno por ID de usuario")
async def get_user_allergen(
    user_id: int = Path(..., title="ID del usuario"),
    db: AsyncSession = Depends(get_db)
):
    return {"msg": f"Alérgeno del usuario con ID {user_id}"}

@router.put("/{allergen_id}", summary="Actualizar alérgeno ")
async def update_allergen(
    allergen_id: int = Path(..., title="ID del alérgeno"),
    db: AsyncSession = Depends(get_db)
):
    return {"msg": f"Alérgeno con ID {allergen_id} actualizado"}

@router.delete("/{allergen_id}", summary="Eliminar alérgeno")
async def delete_allergen(
    allergen_id: int = Path(..., title="ID del alérgeno"),
    db: AsyncSession = Depends(get_db)
):
    return {"msg": f"Alérgeno con ID {allergen_id} eliminado"}