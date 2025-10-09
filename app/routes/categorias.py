from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db

router = APIRouter(prefix="/categorias", tags=["Categorías"])

@router.get("/list")
async def list_categorias(db: AsyncSession = Depends(get_db)):
    return {"msg": "Lista de todas las categorías"}

@router.get("/{categoria_id}")
async def get_categoria(
    categoria_id: int = Path(..., ge=1, description="ID de la categoría"),
    db: AsyncSession = Depends(get_db),
):
    return {"msg": f"Información de la categoría {categoria_id}"}

@router.post("/")
async def create_categoria(db: AsyncSession = Depends(get_db)):
    return {"msg": "Categoría creada correctamente"}

@router.put("/{categoria_id}")
async def modify_categoria(
    categoria_id: int = Path(..., ge=1, description="ID de la categoría"),
    db: AsyncSession = Depends(get_db),
):
    return {"msg": f"Categoría {categoria_id} modificada"}

@router.put("/{categoria_id}/actualizar")
async def update_categoria(
    categoria_id: int = Path(..., ge=1, description="ID de la categoría"),
    db: AsyncSession = Depends(get_db),
):
    return {"msg": f"Categoría {categoria_id} actualizada"}

@router.delete("/{categoria_id}")
async def delete_categoria(
    categoria_id: int = Path(..., ge=1, description="ID de la categoría"),
    db: AsyncSession = Depends(get_db),
):
    return {"msg": f"Categoría {categoria_id} eliminada"}
