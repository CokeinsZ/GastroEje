from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.models.accessibility_features import AccessibilityFeature
from app.schemas.accessibility_features import (
    AccessibilityFeatureCreate,
    AccessibilityFeatureUpdate,
    AccessibilityFeatureOut,
    AccessibilityFeatureMessageOut
)
from typing import List

router = APIRouter(prefix="/accessibilidad", tags=["Accesibilidad"])

# Endpoints
@router.get("/list", response_model=List[AccessibilityFeatureOut])
async def list_accessibility_features(db: AsyncSession = Depends(get_db)):
    """Listar todas las características de accesibilidad"""
    result = await db.execute(select(AccessibilityFeature))
    features = result.scalars().all()
    return features

@router.get("/{feature_id}", response_model=AccessibilityFeatureOut)
async def get_accessibility_feature(
    feature_id: int = Path(..., description="ID de la característica de accesibilidad"),
    db: AsyncSession = Depends(get_db)
):
    """Mostrar información de una característica de accesibilidad específica"""
    result = await db.execute(
        select(AccessibilityFeature).where(AccessibilityFeature.id == feature_id)
    )
    feature = result.scalar_one_or_none()
    
    if not feature:
        raise HTTPException(status_code=404, detail="Accessibility feature not found")
    
    return feature

@router.post("/", response_model=AccessibilityFeatureMessageOut, status_code=201)
async def create_accessibility_feature(
    feature_data: AccessibilityFeatureCreate,
    db: AsyncSession = Depends(get_db)
):
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
    
    return {
        "message": "Accessibility feature created successfully", 
        "feature_id": new_feature.id
    }

@router.put("/{feature_id}", response_model=AccessibilityFeatureOut)
async def update_accessibility_feature(
    feature_data: AccessibilityFeatureUpdate,
    feature_id: int = Path(..., description="ID de la característica a actualizar"),
    db: AsyncSession = Depends(get_db)
):
    """Modificar/Actualizar una característica de accesibilidad"""
    result = await db.execute(
        select(AccessibilityFeature).where(AccessibilityFeature.id == feature_id)
    )
    feature = result.scalar_one_or_none()
    
    if not feature:
        raise HTTPException(status_code=404, detail="Accessibility feature not found")
    
    # Actualizar solo los campos proporcionados
    update_data = feature_data.dict(exclude_unset=True)
    
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

@router.delete("/{feature_id}", response_model=AccessibilityFeatureMessageOut)
async def delete_accessibility_feature(
    feature_id: int = Path(..., description="ID de la característica a eliminar"),
    db: AsyncSession = Depends(get_db)
):
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