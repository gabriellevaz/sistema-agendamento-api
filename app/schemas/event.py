from pydantic import BaseModel, ConfigDict
from typing import Optional

# --- SCHEMAS PARA EVENTOS (Consultas/Aulas) ---
class EventBase(BaseModel):
    title: str
    description: Optional[str] = None
    duration_minutes: int
    cancellation_limit_hours: int = 24
    status: str = "active"
    is_repeatable: int = 1
    company_id: str

class EventCreate(EventBase):
    pass

class EventResponse(EventBase):
    id: str
    
    model_config = ConfigDict(from_attributes=True)


# --- SCHEMAS PARA DISPONIBILIDADE (Regras de Horários) ---
class AvailabilityBase(BaseModel):
    day_of_week: int
    start_time: str
    end_time: str
    event_id: str

class AvailabilityCreate(AvailabilityBase):
    pass

class AvailabilityResponse(AvailabilityBase):
    id: str
    
    model_config = ConfigDict(from_attributes=True)


# --- SCHEMAS PARA BLOQUEIOS DE CALENDÁRIO ---
class CalendarBlockBase(BaseModel):
    start_datetime: str
    end_datetime: str
    reason: Optional[str] = None
    company_id: str
    event_id: Optional[str] = None

class CalendarBlockCreate(CalendarBlockBase):
    force_cancel: bool = False # Se for True, avisa o backend para cancelar agendamentos que existam neste horário

class CalendarBlockResponse(CalendarBlockBase):
    id: str
    
    model_config = ConfigDict(from_attributes=True)