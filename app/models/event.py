import uuid
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship # Importante para navegar entre objetos
from app.core.database import Base

def generate_uuid():
    return str(uuid.uuid4())

class Event(Base):
    __tablename__ = "events"

    id = Column(String, primary_key=True, default=generate_uuid)
    company_id = Column(String, ForeignKey("companies.id"), nullable=False, index=True) # Index adicionado
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    duration_minutes = Column(Integer, nullable=False)
    cancellation_limit_hours = Column(Integer, default=24)
    status = Column(String, default="active")
    is_repeatable = Column(Integer, default=1)
    
    # Adicionando relacionamento para deletar disponibilidades junto com o evento
    availabilities = relationship("Availability", backref="event", cascade="all, delete-orphan")

class Availability(Base):
    __tablename__ = "availabilities"

    id = Column(String, primary_key=True, default=generate_uuid)
    event_id = Column(String, ForeignKey("events.id", ondelete="CASCADE"), nullable=False, index=True)
    day_of_week = Column(Integer, nullable=False)
    start_time = Column(String, nullable=False)
    end_time = Column(String, nullable=False)