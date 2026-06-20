from pydantic import BaseModel, ConfigDict
from typing import Optional

class BookingBase(BaseModel):
    company_id: str
    customer_id: str
    event_id: str
    scheduled_time: str # Ex: "2026-06-25T14:00:00"

class BookingCreate(BookingBase):
    pass

class BookingResponse(BookingBase):
    id: str
    status: str
    qr_code_token: str
    reminder_48h_sent: int
    reminder_24h_sent: int
    created_at: str
    
    model_config = ConfigDict(from_attributes=True)