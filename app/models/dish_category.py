from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class DishCategory(Base):
  __tablename__ = "dish_category"

  dish_id = Column(Integer, ForeignKey("dishes.dish_id"), primary_key=True)
  category_id = Column(Integer, ForeignKey("categories.category_id"), primary_key=True)

  dish = relationship("Dish", back_populates="categories")
  category = relationship("Category", back_populates="dishes")
