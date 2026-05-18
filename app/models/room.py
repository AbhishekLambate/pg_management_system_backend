from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    room_number = Column(String(20), nullable=False)
    building_id = Column(Integer, ForeignKey("buildings.id", ondelete="CASCADE"), nullable=False, index=True)
    floor = Column(Integer, default=1, nullable=False)
    room_type = Column(String(20), default="single", nullable=False)  # single/double/triple/dormitory
    capacity = Column(Integer, default=1, nullable=False)
    rent_amount = Column(Float, nullable=False)
    status = Column(String(20), default="vacant", nullable=False)  # vacant/occupied/maintenance
    amenities = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    building = relationship("Building", back_populates="rooms")
