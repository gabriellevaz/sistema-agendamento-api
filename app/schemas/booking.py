from pydantic import BaseModel, ConfigDict
from typing import Optional

# --- SCHEMAS PARA AGENDAMENTOS ---
class BookingBase(BaseModel):
    # Removido: company_id e customer_id.
    # O Backend irá injetá-los a partir do token e do contexto do usuário.
    event_id: str
    scheduled_time: str # Ex: "2026-06-25T14:00:00"

class BookingCreate(BookingBase):
    pass

class BookingResponse(BookingBase):
    id: str
    company_id: str
    customer_id: str
    status: str
    qr_code_token: str
    reminder_48h_sent: int
    reminder_24h_sent: int
    created_at: str
    
    model_config = ConfigDict(from_attributes=True)