from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from app.models.reviews import Review, RatingEnum
from app.models.users import User
from app.models.establishments import Establishment
from app.schemas.review import ReviewCreate, ReviewUpdate


async def create_review(db: AsyncSession, review_data: ReviewCreate):
    """Crear una nueva reseña"""
    # Verificar que el usuario existe
    user_result = await db.execute(
        select(User).where(User.user_id == review_data.user_id)
    )
    if not user_result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="User not found")
    
    # Verificar que el establecimiento existe
    est_result = await db.execute(
        select(Establishment).where(Establishment.establishment_id == review_data.establishment_id)
    )
    if not est_result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Establishment not found")
    
    # Verificar que el usuario no haya creado ya una reseña para este establecimiento
    existing_review = await db.execute(
        select(Review).where(
            Review.user_id == review_data.user_id,
            Review.establishment_id == review_data.establishment_id
        )
    )
    if existing_review.scalar_one_or_none():
        raise HTTPException(
            status_code=400, 
            detail="User has already reviewed this establishment"
        )
    
    # Convertir string a enum
    try:
        rating_enum = RatingEnum[f"{'ONE' if review_data.rating == '1' else 'TWO' if review_data.rating == '2' else 'THREE' if review_data.rating == '3' else 'FOUR' if review_data.rating == '4' else 'FIVE'}"]
    except KeyError:
        raise HTTPException(status_code=400, detail="Invalid rating value")
    
    # Crear la reseña
    new_review = Review(
        user_id=review_data.user_id,
        establishment_id=review_data.establishment_id,
        rating=rating_enum,
        comment=review_data.comment,
        img=review_data.img
    )
    
    db.add(new_review)
    await db.commit()
    await db.refresh(new_review)
    
    return new_review


async def get_all_reviews(db: AsyncSession):
    """Obtener todas las reseñas"""
    result = await db.execute(select(Review))
    return result.scalars().all()


async def get_review_by_user_and_establishment(db: AsyncSession, user_id: int, establishment_id: int):
    """Obtener una reseña específica por usuario y establecimiento"""
    result = await db.execute(
        select(Review).where(
            Review.user_id == user_id,
            Review.establishment_id == establishment_id
        )
    )
    review = result.scalar_one_or_none()
    
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    
    return review


async def get_reviews_by_establishment(db: AsyncSession, establishment_id: int):
    """Obtener todas las reseñas de un establecimiento"""
    result = await db.execute(
        select(Review).where(Review.establishment_id == establishment_id)
    )
    return result.scalars().all()


async def get_reviews_by_user(db: AsyncSession, user_id: int):
    """Obtener todas las reseñas de un usuario"""
    result = await db.execute(
        select(Review).where(Review.user_id == user_id)
    )
    return result.scalars().all()


async def update_review(db: AsyncSession, user_id: int, establishment_id: int, review_data: ReviewUpdate):
    """Actualizar una reseña"""
    result = await db.execute(
        select(Review).where(
            Review.user_id == user_id,
            Review.establishment_id == establishment_id
        )
    )
    review = result.scalar_one_or_none()
    
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    
    # Actualizar solo los campos proporcionados
    update_data = review_data.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        if field == "rating" and value:
            # Convertir string a enum
            try:
                value = RatingEnum[f"{'ONE' if value == '1' else 'TWO' if value == '2' else 'THREE' if value == '3' else 'FOUR' if value == '4' else 'FIVE'}"]
            except KeyError:
                raise HTTPException(status_code=400, detail="Invalid rating value")
        setattr(review, field, value)
    
    await db.commit()
    await db.refresh(review)
    
    return review


async def delete_review(db: AsyncSession, user_id: int, establishment_id: int):
    """Eliminar una reseña"""
    result = await db.execute(
        select(Review).where(
            Review.user_id == user_id,
            Review.establishment_id == establishment_id
        )
    )
    review = result.scalar_one_or_none()
    
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    
    await db.delete(review)
    await db.commit()
    
    return {"message": "Review deleted successfully"}
