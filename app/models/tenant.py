from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float, Date, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Tenant(Base):
    __tablename__ = "tenants"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, unique=True, index=True)
    room_id = Column(Integer, ForeignKey("rooms.id", ondelete="SET NULL"), nullable=True, index=True)

    # Personal info
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=False)
    alternate_phone = Column(String(20), nullable=True)
    email = Column(String(100), nullable=True)
    permanent_address = Column(Text, nullable=True)

    # Emergency contact
    emergency_contact_name = Column(String(100), nullable=True)
    emergency_contact_phone = Column(String(20), nullable=True)

    # ID Proof
    id_proof_type = Column(String(30), nullable=True)   # aadhar/passport/driving_license/voter_id
    id_proof_number = Column(String(50), nullable=True)

    # Stay details
    move_in_date = Column(Date, nullable=True)
    move_out_date = Column(Date, nullable=True)
    deposit_amount = Column(Float, default=0.0, nullable=False)
    status = Column(String(20), default="active", nullable=False)  # active/checked_out/on_notice

    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", backref="tenant", uselist=False)
    room = relationship("Room", backref="tenants")
