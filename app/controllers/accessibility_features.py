from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from app.models.accessibility_features import AccessibilityFeature
from app.schemas.accessibility_features import AccessibilityFeatureCreate, AccessibilityFeatureUpdate


async def get_all_accessibility_features(db: AsyncSession):
    """Obtener todas las características de accesibilidad"""
    result = await db.execute(select(AccessibilityFeature))
    return result.scalars().all()


async def get_accessibility_feature_by_id(db: AsyncSession, feature_id: int):
    """Obtener una característica de accesibilidad por ID"""
    result = await db.execute(
        select(AccessibilityFeature).where(AccessibilityFeature.id == feature_id)
    )
    feature = result.scalar_one_or_none()
    
    if not feature:
        raise HTTPException(status_code=404, detail="Accessibility feature not found")
    
    return feature


async def create_accessibility_feature(db: AsyncSession, feature_data: AccessibilityFeatureCreate):
    """Crear una nueva característica de accesibilidad"""
    # Verificar si ya existe una característica con el mismo nombre para el mismo establecimiento
    result = await db.execute(
        select(AccessibilityFeature).where(
            AccessibilityFeature.establishment_id == feature_data.establishment_id,
            AccessibilityFeature.name == feature_data.name
        )
    )
    existing_feature = result.scalar_one_or_none()
    
    if existing_feature:
        raise HTTPException(
            status_code=400, 
            detail="Accessibility feature with this name already exists for this establishment"
        )
    
    # Crear nueva característica de accesibilidad
    new_feature = AccessibilityFeature(
        establishment_id=feature_data.establishment_id,
        name=feature_data.name,
        description=feature_data.description
    )
    
    db.add(new_feature)
    await db.commit()
    await db.refresh(new_feature)
    
    return new_feature


async def update_accessibility_feature(db: AsyncSession, feature_id: int, feature_data: AccessibilityFeatureUpdate):
    """Actualizar una característica de accesibilidad"""
    result = await db.execute(
        select(AccessibilityFeature).where(AccessibilityFeature.id == feature_id)
    )
    feature = result.scalar_one_or_none()
    
    if not feature:
        raise HTTPException(status_code=404, detail="Accessibility feature not found")
    
    # Actualizar solo los campos proporcionados
    update_data = feature_data.model_dump(exclude_unset=True)
    
    # Si se está actualizando el nombre, verificar que no exista otro con el mismo nombre en el mismo establecimiento
    if 'name' in update_data and update_data['name'] != feature.name:
        result = await db.execute(
            select(AccessibilityFeature).where(
                AccessibilityFeature.establishment_id == feature.establishment_id,
                AccessibilityFeature.name == update_data['name'],
                AccessibilityFeature.id != feature_id
            )
        )
        existing_feature = result.scalar_one_or_none()
        
        if existing_feature:
            raise HTTPException(
                status_code=400, 
                detail="Accessibility feature with this name already exists for this establishment"
            )
    
    for field, value in update_data.items():
        setattr(feature, field, value)
    
    await db.commit()
    await db.refresh(feature)
    
    return feature


async def delete_accessibility_feature(db: AsyncSession, feature_id: int):
    """Eliminar una característica de accesibilidad"""
    result = await db.execute(
        select(AccessibilityFeature).where(AccessibilityFeature.id == feature_id)
    )
    feature = result.scalar_one_or_none()
    
    if not feature:
        raise HTTPException(status_code=404, detail="Accessibility feature not found")
    
    await db.delete(feature)
    await db.commit()
    
    return {"message": "Accessibility feature deleted successfully"}
