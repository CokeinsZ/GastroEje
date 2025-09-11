from sqlalchemy import *
from sqlalchemy.orm import *
from app.database import Base

class Establishment(Base):
  __tablename__ = "establishments"

  establishment_id = Column(Integer, primary_key=True, index=True)
  NIT = Column(String(16), primary_key=True, index=True)
  name = Column(String(32), nullable=False)
  description = Column(Text)
  sustainability_points = Column(Integer, default=0)
  address = Column(Text)
  mean_waiting_time = Column(Float)
  opening_hour = Column(Time)
  closing_hour = Column(Time)
  phone_number = Column(String(12))
  website = Column(String(255))
  logo = Column(String(255))

  # Relaciones
  menus = relationship("Menu", back_populates="establishment")
  reservations = relationship("Reservation", back_populates="establishment")
  reviews = relationship("Review", back_populates="establishment")
  categories = relationship("EstablishmentCategory", back_populates="establishment")
  accessibility_features = relationship("AccessibilityFeature", back_populates="establishment")
