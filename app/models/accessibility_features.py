from sqlalchemy import *
from sqlalchemy.orm import *
from app.database import Base

class AccessibilityFeature(Base):
    __tablename__ = "accessibility_features"

    id = Column(Integer, primary_key=True, index=True)
    establishment_id = Column(Integer, ForeignKey("establishments.establishment_id"), nullable=False)

    name = Column(String(32), nullable=False)
    description = Column(Text)

    # Relaciones
    establishment = relationship("Establishment", back_populates="accessibility_features")
