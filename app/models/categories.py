from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

#from app.database import Base

class Category():
    __tablename__ = 'categories'

    category_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(32), nullable=False)
    description = Column(String, nullable=True)

    # Relación con platos (dishes)
    dishes = relationship("Dish", secondary="dish_category", back_populates="categories")

    # Relación con establecimientos
    establishments = relationship("EstablishmentCategory", back_populates="category")
