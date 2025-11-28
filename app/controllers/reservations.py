from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from app.models.reservations import Reservation, ReservationStatus
from app.models.users import User
from app.models.establishments import Establishment
from app.schemas.reservations import ReservationsCreate, ReservationsUpdate


async def create_reservation(db: AsyncSession, reservation_data: ReservationsCreate):
    """Crear una nueva reserva"""
    # Verificar que el usuario existe
    user_result = await db.execute(
        select(User).where(User.user_id == reservation_data.user_id)
    )
    if not user_result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="User not found")
    
    # Verificar que el establecimiento existe
    est_result = await db.execute(
        select(Establishment).where(Establishment.establishment_id == reservation_data.establishment_id)
    )
    if not est_result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Establishment not found")
    
    # Crear la reserva
    new_reservation = Reservation(
        user_id=reservation_data.user_id,
        establishment_id=reservation_data.establishment_id,
        date=reservation_data.date,
        people_count=reservation_data.people_count,
        status=ReservationStatus.pending
    )
    
    db.add(new_reservation)
    await db.commit()
    await db.refresh(new_reservation)
    
    return new_reservation


async def get_all_reservations(db: AsyncSession):
    """Obtener todas las reservas"""
    result = await db.execute(select(Reservation))
    return result.scalars().all()


async def get_reservation_by_id(db: AsyncSession, reservation_id: int):
    """Obtener una reserva específica por ID"""
    result = await db.execute(
        select(Reservation).where(Reservation.reservation_id == reservation_id)
    )
    reservation = result.scalar_one_or_none()
    
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    
    return reservation


async def update_reservation(db: AsyncSession, reservation_id: int, reservation_data: ReservationsUpdate):
    """Actualizar una reserva"""
    result = await db.execute(
        select(Reservation).where(Reservation.reservation_id == reservation_id)
    )
    reservation = result.scalar_one_or_none()
    
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    
    # Actualizar solo los campos proporcionados
    update_data = reservation_data.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        if field == "status" and isinstance(value, str):
            # Convertir string a enum
            value = ReservationStatus[value]
        setattr(reservation, field, value)
    
    await db.commit()
    await db.refresh(reservation)
    
    return reservation


async def cancel_reservation(db: AsyncSession, reservation_id: int):
    """Cancelar una reserva (cambiar estado a cancelled)"""
    result = await db.execute(
        select(Reservation).where(Reservation.reservation_id == reservation_id)
    )
    reservation = result.scalar_one_or_none()
    
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    
    reservation.status = ReservationStatus.cancelled
    
    await db.commit()
    await db.refresh(reservation)
    
    return reservation


async def delete_reservation(db: AsyncSession, reservation_id: int):
    """Eliminar una reserva completamente"""
    result = await db.execute(
        select(Reservation).where(Reservation.reservation_id == reservation_id)
    )
    reservation = result.scalar_one_or_none()
    
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    
    await db.delete(reservation)
    await db.commit()
    
    return {"message": "Reservation deleted successfully"}


async def get_reservations_by_user(db: AsyncSession, user_id: int):
    """Obtener todas las reservas de un usuario"""
    result = await db.execute(
        select(Reservation).where(Reservation.user_id == user_id)
    )
    return result.scalars().all()


async def get_reservations_by_establishment(db: AsyncSession, establishment_id: int):
    """Obtener todas las reservas de un establecimiento"""
    result = await db.execute(
        select(Reservation).where(Reservation.establishment_id == establishment_id)
    )
    return result.scalars().all()
