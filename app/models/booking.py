import uuid
from sqlalchemy import Column, String, Integer, ForeignKey, Index
from sqlalchemy.sql import func
from app.core.database import Base

def generate_uuid():
    return str(uuid.uuid4())

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(String, primary_key=True, default=generate_uuid)
    company_id = Column(String, ForeignKey("companies.id"), nullable=False)
    customer_id = Column(String, ForeignKey("users.id"), nullable=False)
    event_id = Column(String, ForeignKey("events.id"), nullable=False)
    scheduled_time = Column(String, nullable=False) # Ex: "2026-06-25T14:00:00"
    status = Column(String, default="confirmed")
    qr_code_token = Column(String, nullable=False, unique=True)
    reminder_48h_sent = Column(Integer, default=0)
    reminder_24h_sent = Column(Integer, default=0)
    created_at = Column(String, server_default=func.now())

# Proteção contra Race Conditions no SQLite (Ninguém agenda no mesmo horário e no mesmo evento se estiver confirmado)
Index("idx_unique_booking_slot", Booking.event_id, Booking.scheduled_time, unique=True, sqlite_where=(Booking.status == 'confirmed'))