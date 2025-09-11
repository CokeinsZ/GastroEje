from sqlalchemy import Column, Integer, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from app.database import Base

class DishAllergen(Base):
    __tablename__ = "dish_allergen"

    dish_id     = Column(Integer, ForeignKey("dishes.dish_id"), primary_key=True, index=True)
    allergen_id = Column(Integer, ForeignKey("allergens.allergen_id"), primary_key=True, index=True)

    __table_args__ = {
        PrimaryKeyConstraint('dish_id', 'allergen_id')
    }


#relaciones
    dish     = relationship("Dish",      back_populates="allergens")
    allergen = relationship("Allergens", back_populates="dishes")
