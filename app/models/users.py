from sqlalchemy import *
from sqlalchemy.orm import *
from datetime import datetime, timezone
import enum
from app.database import Base

class UserRole(enum.Enum):
  admin = "admin"
  user = "user"

class UserStatus(enum.Enum):
  ACTIVE = "active"
  INACTIVE = "inactive"
  NOT_VERIFIED = "not_verified"
  BANNED = "banned"

class User(Base):
  __tablename__ = "users"

  user_id = Column(Integer, primary_key=True, index=True)
  role = Column(Enum(UserRole), nullable=False)
  name = Column(String(32), nullable=False)
  last_name = Column(String(32))
  email = Column(String(255), unique=True, nullable=False, index=True)
  password = Column(String(255), nullable=False)
  phone = Column(String(13))
  status = Column(Enum(UserStatus), default=UserStatus.active)
  created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
  updated_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

  # Relaciones
  reservations = relationship("Reservation", back_populates="user")
  reviews = relationship("Review", back_populates="user")
  allergens = relationship("UserAllergen", back_populates="user")