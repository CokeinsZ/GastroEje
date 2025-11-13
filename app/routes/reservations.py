# app/routers/reservas.py
from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.database import get_session
from app.schemas.reservations import ReservationsCreate, ReservationUpdate, ReservationOut
from app.schemas.category import MessageOut 

from app.controllers.reservations import *

router = APIRouter(prefix="/reservas", tags=["Reservas"])


# -----------------------
# LISTAR RESERVAS → GET
# -----------------------
@router.get("/list", response_model=List[ReservationOut])
async def list_reservas(db: AsyncSession = Depends(get_session)):
    return await get_reservations(db)


# -----------------------
# CANCELAR RESERVA → DELETE
# -----------------------
@router.delete("/{reserva_id}", response_model=MessageOut)
async def cancelar_reserva(
    reserva_id: int = Path(..., ge=1, description="ID de la reserva"),
    db: AsyncSession = Depends(get_session),
):
    deleted = await delete_reservation(db, reserva_id)
    return {"msg": "Reserva eliminada correctamente"} if deleted else {"msg": "Reserva no encontrada"}


# -----------------------
# ACTUALIZAR RESERVA → POST
# -----------------------
@router.post("/{reserva_id}/actualizar", response_model=ReservationOut)
async def actualizar_reserva(
    reservation: ReservationUpdate,
    reserva_id: int = Path(..., ge=1, description="ID de la reserva"),
    db: AsyncSession = Depends(get_session)
):
    return await update_reservation(db, reserva_id, reservation)


# -----------------------
# MOSTRAR RESERVA → GET
# -----------------------
@router.get("/{reserva_id}", response_model=ReservationOut)
async def get_reserva(
    reserva_id: int = Path(..., ge=1, description="ID de la reserva"),
    db: AsyncSession = Depends(get_session)
):
    return await get_reservation_by_id(db, reserva_id)


# -----------------------
# REGISTRAR RESERVA → POST
# -----------------------
@router.post("/", response_model=ReservationOut, status_code=201)
async def registrar_reserva(
    reservation: ReservationsCreate,
    db: AsyncSession = Depends(get_session)
):
    return await create_reservation(db, reservation)
