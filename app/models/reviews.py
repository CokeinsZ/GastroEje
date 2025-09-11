from sqlalchemy import *
from sqlalchemy.orm import *
from datetime import datetime, timezone
import enum
from app.database import Base

class RatingEnum(enum.Enum):
    ONE = "1"
    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"


class Review(Base):
    __tablename__ = "reviews"

    # Claves primarias compuestas (user_id + establishment_id)
    user_id = Column(Integer, ForeignKey("users.user_id"), primary_key=True)
    establishment_id = Column(Integer, ForeignKey("establishments.establishment_id"), primary_key=True)

    rating = Column(Enum(RatingEnum), nullable=False)
    comment = Column(Text)
    img = Column(String(255))
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))

    # Relaciones
    user = relationship("User", back_populates="reviews")
    establishment = relationship("Establishment", back_populates="reviews")
