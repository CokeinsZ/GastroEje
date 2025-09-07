# models/dish_category.py
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

class DishCategory:
  __tablename__ = "dish_category"

  dish_id = Column(Integer, ForeignKey("dishes.dish_id"), primary_key=True)
  category_id = Column(Integer, ForeignKey("categories.category_id"), primary_key=True)

  dish = relationship("Dish", back_populates="categories")
  category = relationship("Category", back_populates="dishes")
