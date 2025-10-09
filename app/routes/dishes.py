# app/routers/platos.py
from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db

router = APIRouter(prefix="/platos", tags=["Platos"])

# Listar platos → GET
@router.get("/list")
async def list_platos(db: AsyncSession = Depends(get_db)):
    return {"msg": "Lista de todos los platos"}

# Mostrar info de un plato → GET
@router.get("/{plato_id}")
async def get_plato(
    plato_id: int = Path(..., ge=1, description="ID del plato"),
    db: AsyncSession = Depends(get_db),
):
    return {"msg": f"Información del plato {plato_id}"}

# Modificar o actualizar plato → PUT
@router.put("/{plato_id}")
async def update_plato(
    plato_id: int = Path(..., ge=1, description="ID del plato"),
    db: AsyncSession = Depends(get_db),
):
    return {"msg": f"Plato {plato_id} actualizado"}

# Crear platos → POST
@router.post("/")
async def create_plato(db: AsyncSession = Depends(get_db)):
    return {"msg": "Plato creado correctamente"}

# Eliminar platos → DELETE
@router.delete("/{plato_id}")
async def delete_plato(
    plato_id: int = Path(..., ge=1, description="ID del plato"),
    db: AsyncSession = Depends(get_db),
):
    return {"msg": f"Plato {plato_id} eliminado"}

# Mostrar alérgeno → POST
@router.post("/{plato_id}/alergeno")
async def mostrar_alergeno(
    plato_id: int = Path(..., ge=1, description="ID del plato"),
    db: AsyncSession = Depends(get_db),
):
    return {"msg": f"Alérgenos del plato {plato_id}"}
