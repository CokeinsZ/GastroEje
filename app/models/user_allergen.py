from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class UserAllergen(Base):
    __tablename__ = "user_allergen"

    user_id     = Column(Integer, ForeignKey("users.user_id"), primary_key=True, index=True)
    allergen_id = Column(Integer, ForeignKey("allergens.allergen_id"), primary_key=True, index=True)

# Relaciones
    user     = relationship("User",      back_populates="allergens")
    allergen = relationship("Allergens", back_populates="users")
