from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.accessibility_features import (
    AccessibilityFeatureCreate,
    AccessibilityFeatureUpdate,
    AccessibilityFeatureOut,
    AccessibilityFeatureMessageOut
)
from app.controllers.accessibility_features import (
    get_all_accessibility_features,
    get_accessibility_feature_by_id,
    create_accessibility_feature,
    update_accessibility_feature,
    delete_accessibility_feature
)
from typing import List

router = APIRouter(prefix="/accessibilidad", tags=["Accesibilidad"])

# Endpoints
@router.get("/list", response_model=List[AccessibilityFeatureOut])
async def list_accessibility_features(db: AsyncSession = Depends(get_db)):
    """Listar todas las características de accesibilidad"""
    return await get_all_accessibility_features(db)

@router.get("/{feature_id}", response_model=AccessibilityFeatureOut)
async def get_accessibility_feature(
    feature_id: int = Path(..., description="ID de la característica de accesibilidad"),
    db: AsyncSession = Depends(get_db)
):
    """Mostrar información de una característica de accesibilidad específica"""
    return await get_accessibility_feature_by_id(db, feature_id)

@router.post("/", response_model=AccessibilityFeatureMessageOut, status_code=201)
async def create_accessibility_feature_route(
    feature_data: AccessibilityFeatureCreate,
    db: AsyncSession = Depends(get_db)
):
    """Crear una nueva característica de accesibilidad"""
    new_feature = await create_accessibility_feature(db, feature_data)
    return {
        "message": "Accessibility feature created successfully", 
        "feature_id": new_feature.id
    }

@router.put("/{feature_id}", response_model=AccessibilityFeatureOut)
async def update_accessibility_feature_route(
    feature_data: AccessibilityFeatureUpdate,
    feature_id: int = Path(..., description="ID de la característica a actualizar"),
    db: AsyncSession = Depends(get_db)
):
    """Modificar/Actualizar una característica de accesibilidad"""
    return await update_accessibility_feature(db, feature_id, feature_data)

@router.delete("/{feature_id}", response_model=AccessibilityFeatureMessageOut)
async def delete_accessibility_feature_route(
    feature_id: int = Path(..., description="ID de la característica a eliminar"),
    db: AsyncSession = Depends(get_db)
):
    """Eliminar una característica de accesibilidad"""
    return await delete_accessibility_feature(db, feature_id)