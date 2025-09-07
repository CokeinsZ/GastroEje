from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
#from app.database import Base

class Dish():
    __tablename__ = 'dishes'

    dish_id = Column(Integer, primary_key=True, index=True)
    menu_id = Column(Integer, ForeignKey('menus.menu_id'))
    name = Column(String(32), nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    img = Column(String(255), nullable=True)

    # Relaciones
    menu = relationship("Menu", back_populates="dishes")
    categories = relationship("Category", secondary="dish_category", back_populates="dishes")
    allergens = relationship("DishAllergen", back_populates="dish")
