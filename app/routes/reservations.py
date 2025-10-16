# app/routers/reservas.py
from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.database import get_db
from app.schemas.reservations import ReservationsCreate, ReservationsOut
from app.schemas.category import MessageOut

router = APIRouter(prefix="/reservas", tags=["Reservas"])

# Listar reservas → GET
@router.get("/list", response_model=List[ReservationsOut])
async def list_reservas(db: AsyncSession = Depends(get_db)):
    """Obtener lista de todas las reservas"""
    return []

# Cancelar reservas → DELETE
@router.delete("/{reserva_id}", response_model=MessageOut)
async def cancelar_reserva(
    reserva_id: int = Path(..., ge=1, description="ID de la reserva"),
    db: AsyncSession = Depends(get_db),
):
    """Cancelar una reserva"""
    return {"msg": f"Reserva {reserva_id} cancelada"}

# Actualizar reserva → POST (según tu requerimiento)
@router.post("/{reserva_id}/actualizar", response_model=ReservationsOut)
async def actualizar_reserva(
    reservation: ReservationsCreate,
    reserva_id: int = Path(..., ge=1, description="ID de la reserva"),
    db: AsyncSession = Depends(get_db),
):
    """Actualizar una reserva existente"""
    return {"msg": f"Reserva {reserva_id} actualizada"}

# Mostrar info de la reserva → GET
@router.get("/{reserva_id}", response_model=ReservationsOut)
async def get_reserva(
    reserva_id: int = Path(..., ge=1, description="ID de la reserva"),
    db: AsyncSession = Depends(get_db),
):
    """Obtener información de una reserva específica"""
    return {"msg": f"Información de la reserva {reserva_id}"}

# Registrar reserva → POST
@router.post("/", response_model=ReservationsOut, status_code=201)
async def registrar_reserva(
    reservation: ReservationsCreate,
    db: AsyncSession = Depends(get_db)
):
    """Registrar una nueva reserva"""
    return {"msg": "Reserva registrada correctamente"}
