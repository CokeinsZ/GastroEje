from pydantic import BaseModel, ConfigDict
from typing import Optional

# Esquemas base
class AccessibilityFeatureBase(BaseModel):
    name: str
    description: Optional[str] = None

class AccessibilityFeatureCreate(AccessibilityFeatureBase):
    establishment_id: int

class AccessibilityFeatureUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

# Esquemas de respuesta
class AccessibilityFeatureOut(AccessibilityFeatureBase):
    id: int
    establishment_id: int
    
    model_config = ConfigDict(from_attributes=True)

class AccessibilityFeatureMessageOut(BaseModel):
    message: str
    feature_id: Optional[int] = None