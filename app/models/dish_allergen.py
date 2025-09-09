from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

class DishAllergen():
    __tablename__ = "dish_allergen"

    dish_id     = Column(Integer, ForeignKey("dishes.dish_id"), primary_key=True, index=True)
    allergen_id = Column(Integer, ForeignKey("allergens.allergen_id"), primary_key=True, index=True)


#relaciones
    dish     = relationship("Dish",      back_populates="allergens")
    allergen = relationship("Allergens", back_populates="dishes")
