from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional

class UserBase(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    birth_date: str
    role: str = "customer" # Default já como cliente

class UserCreate(UserBase):
    password: str
    # company_id foi removido daqui, pois o servidor injetará o company_id correto

class UserResponse(UserBase):
    id: str
    company_id: str # O sistema devolve o company_id para o front saber onde ele está
    created_at: str
    
    model_config = ConfigDict(from_attributes=True)