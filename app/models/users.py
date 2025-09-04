from sqlalchemy import *
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import enum

class UserStatus(enum.Enum):
  ACTIVE = "active"
  INACTIVE = "inactive"
  NOT_VERIFIED = "not_verified"
  BANNED = "banned"

class Users():
  __tablename__ = "users"

  user_id = Column(Integer, primary_key=True, index=True)
  role = Column(String)
  name = Column(String, nullable=False)
  last_name = Column(String)
  email = Column(String, nullable=False, unique=True, index=True)
  password = Column(String, nullable=False)
  phone = Column(String)
  status = Column(Enum(UserStatus), nullable=False, default=UserStatus.NOT_VERIFIED)
  created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
  updated_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))