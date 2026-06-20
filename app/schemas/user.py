from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional

class UserBase(BaseModel):
    name: str
    email: EmailStr  # O Pydantic já valida automaticamente se tem '@' e '.com'
    phone: Optional[str] = None
    birth_date: str
    role: str
    company_id: Optional[str] = None

class UserCreate(UserBase):
    password: str # O Frontend manda a senha limpa, nós vamos transformar em hash no backend

class UserResponse(UserBase):
    id: str
    created_at: str
    
    # Repare que NÃO incluímos a senha aqui. Ela nunca volta pro Front!
    model_config = ConfigDict(from_attributes=True)