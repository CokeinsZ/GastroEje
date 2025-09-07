from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
#from app.database import Base

class Menu():
    __tablename__ = 'menus'

    menu_id = Column(Integer, primary_key=True, index=True)
    establishment_id = Column(Integer, ForeignKey('establishments.establishment_id'))
    title = Column(String(32), nullable=False)

    # Relaciones
    establishment = relationship("Establishment", back_populates="menus")
    dishes = relationship("Dish", back_populates="menu")
