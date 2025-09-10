from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

class Allergens():
    __tablename__ = "allergens"

    allergen_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(32), nullable=False)

    dishes = relationship("DishAllergen", back_populates="allergen")
    users = relationship("UserAllergen", back_populates="allergen")
