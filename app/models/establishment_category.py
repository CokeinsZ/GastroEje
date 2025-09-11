from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class EstablishmentCategory(Base):
  __tablename__ = "establishment_category"

  establishment_id = Column(Integer, ForeignKey("establishments.establishment_id"), primary_key=True)
  category_id = Column(Integer, ForeignKey("categories.category_id"), primary_key=True)

  establishment = relationship("Establishment", back_populates="categories")
  category = relationship("Category", back_populates="establishments")
