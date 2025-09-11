from sqlalchemy import *
from sqlalchemy.orm import *
from datetime import datetime, timezone
import enum
from app.database import Base

class ReservationStatus(enum.Enum):
  pending = "pending"
  confirmed = "confirmed"
  cancelled = "cancelled"

class Reservation(Base):
  __tablename__ = "reservations"

  reservation_id = Column(Integer, primary_key=True, index=True)
  user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
  establishment_id = Column(Integer, ForeignKey("establishments.establishment_id"), nullable=False)
  date = Column(DateTime, nullable=False)
  people_count = Column(Integer)
  status = Column(Enum(ReservationStatus), default=ReservationStatus.pending)
  created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
  updated_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

  user = relationship("User", back_populates="reservations")
  establishment = relationship("Establishment", back_populates="reservations")
