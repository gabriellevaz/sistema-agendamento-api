import uuid
from sqlalchemy import Column, String, Integer, ForeignKey
from app.core.database import Base

def generate_uuid():
    return str(uuid.uuid4())

class Event(Base):
    __tablename__ = "events"

    id = Column(String, primary_key=True, default=generate_uuid)
    company_id = Column(String, ForeignKey("companies.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    duration_minutes = Column(Integer, nullable=False)
    cancellation_limit_hours = Column(Integer, default=24)
    status = Column(String, default="active")
    is_repeatable = Column(Integer, default=1)

class Availability(Base):
    __tablename__ = "availabilities"

    id = Column(String, primary_key=True, default=generate_uuid)
    event_id = Column(String, ForeignKey("events.id"), nullable=False)
    day_of_week = Column(Integer, nullable=False) # 0 = Domingo, 6 = Sábado
    start_time = Column(String, nullable=False) # "08:00"
    end_time = Column(String, nullable=False) # "18:00"