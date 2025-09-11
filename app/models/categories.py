from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.database import Base

class Category(Base):
    __tablename__ = 'categories'

    category_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(32), nullable=False)
    description = Column(Text, nullable=True)

    # Relación con platos (dishes)
    dishes = relationship("DishCategory", back_populates="category")

    # Relación con establecimientos
    establishments = relationship("EstablishmentCategory", back_populates="category")
