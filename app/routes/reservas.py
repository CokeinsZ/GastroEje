# app/routers/reservas.py
from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db

router = APIRouter(prefix="/reservas", tags=["Reservas"])

# Listar reservas → GET
@router.get("/list")
async def list_reservas(db: AsyncSession = Depends(get_db)):
    return {"msg": "Lista de todas las reservas"}

# Cancelar reservas → DELETE
@router.delete("/{reserva_id}")
async def cancelar_reserva(
    reserva_id: int = Path(..., ge=1, description="ID de la reserva"),
    db: AsyncSession = Depends(get_db),
):
    return {"msg": f"Reserva {reserva_id} cancelada"}

# Actualizar reserva → POST (según tu requerimiento)
@router.post("/{reserva_id}/actualizar")
async def actualizar_reserva(
    reserva_id: int = Path(..., ge=1, description="ID de la reserva"),
    db: AsyncSession = Depends(get_db),
):
    return {"msg": f"Reserva {reserva_id} actualizada"}

# Mostrar info de la reserva → GET
@router.get("/{reserva_id}")
async def get_reserva(
    reserva_id: int = Path(..., ge=1, description="ID de la reserva"),
    db: AsyncSession = Depends(get_db),
):
    return {"msg": f"Información de la reserva {reserva_id}"}

# Registrar reserva → POST
@router.post("/")
async def registrar_reserva(db: AsyncSession = Depends(get_db)):
    return {"msg": "Reserva registrada correctamente"}
