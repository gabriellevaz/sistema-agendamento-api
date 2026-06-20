from pydantic import BaseModel, ConfigDict
from typing import Optional

# --- SCHEMAS PARA EVENTOS ---
class EventBase(BaseModel):
    title: str
    description: Optional[str] = None
    duration_minutes: int
    cancellation_limit_hours: int = 24
    status: str = "active"
    is_repeatable: int = 1
    # Removido company_id daqui, pois será injetado pelo Backend

class EventCreate(EventBase):
    pass

class EventResponse(EventBase):
    id: str
    company_id: str # O id aparece na resposta para leitura, mas não na criação
    
    model_config = ConfigDict(from_attributes=True)

# --- SCHEMAS PARA BLOQUEIOS DE CALENDÁRIO ---
class CalendarBlockBase(BaseModel):
    start_datetime: str
    end_datetime: str
    reason: Optional[str] = None
    event_id: Optional[str] = None
    # Removido company_id daqui pelo mesmo motivo

class CalendarBlockCreate(CalendarBlockBase):
    force_cancel: bool = False

class CalendarBlockResponse(CalendarBlockBase):
    id: str
    company_id: str
    
    model_config = ConfigDict(from_attributes=True)