# app/routers/reservas.py
from fastapi import APIRouter, Depends, Path, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.database import get_db
from app.schemas.reservations import ReservationsCreate, ReservationsUpdate, ReservationsOut, MessageOut
from app.controllers import reservations as reservations_controller

router = APIRouter(prefix="/reservas", tags=["Reservas"])

# Registrar reserva → POST
@router.post("/", response_model=ReservationsOut, status_code=201)
async def registrar_reserva(
    reservation: ReservationsCreate,
    db: AsyncSession = Depends(get_db)
):
    """Registrar una nueva reserva"""
    return await reservations_controller.create_reservation(db, reservation)

# Listar reservas → GET
@router.get("/list", response_model=List[ReservationsOut])
async def list_reservas(db: AsyncSession = Depends(get_db)):
    """Obtener lista de todas las reservas"""
    return await reservations_controller.get_all_reservations(db)

# Mostrar info de la reserva → GET
@router.get("/{reserva_id}", response_model=ReservationsOut)
async def get_reserva(
    reserva_id: int = Path(..., ge=1, description="ID de la reserva"),
    db: AsyncSession = Depends(get_db),
):
    """Obtener información de una reserva específica"""
    return await reservations_controller.get_reservation_by_id(db, reserva_id)

# Actualizar reserva → PUT
@router.put("/{reserva_id}", response_model=ReservationsOut)
async def actualizar_reserva(
    reservation: ReservationsUpdate,
    reserva_id: int = Path(..., ge=1, description="ID de la reserva"),
    db: AsyncSession = Depends(get_db),
):
    """Actualizar una reserva existente"""
    return await reservations_controller.update_reservation(db, reserva_id, reservation)

# Cancelar reservas → PATCH (cambia estado a cancelled)
@router.patch("/{reserva_id}/cancelar", response_model=ReservationsOut)
async def cancelar_reserva(
    reserva_id: int = Path(..., ge=1, description="ID de la reserva"),
    db: AsyncSession = Depends(get_db),
):
    """Cancelar una reserva (cambia el estado a cancelled)"""
    return await reservations_controller.cancel_reservation(db, reserva_id)

# Eliminar reserva → DELETE
@router.delete("/{reserva_id}", response_model=MessageOut)
async def delete_reserva(
    reserva_id: int = Path(..., ge=1, description="ID de la reserva"),
    db: AsyncSession = Depends(get_db),
):
    """Eliminar una reserva completamente"""
    return await reservations_controller.delete_reservation(db, reserva_id)

# Obtener reservas por usuario
@router.get("/usuario/{user_id}", response_model=List[ReservationsOut])
async def get_reservas_by_user(
    user_id: int = Path(..., ge=1, description="ID del usuario"),
    db: AsyncSession = Depends(get_db),
):
    """Obtener todas las reservas de un usuario"""
    return await reservations_controller.get_reservations_by_user(db, user_id)

# Obtener reservas por establecimiento
@router.get("/establecimiento/{establishment_id}", response_model=List[ReservationsOut])
async def get_reservas_by_establishment(
    establishment_id: int = Path(..., ge=1, description="ID del establecimiento"),
    db: AsyncSession = Depends(get_db),
):
    """Obtener todas las reservas de un establecimiento"""
    return await reservations_controller.get_reservations_by_establishment(db, establishment_id)
