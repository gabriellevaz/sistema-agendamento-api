import uuid
from sqlalchemy import Column, String, Integer, ForeignKey, Boolean
from sqlalchemy.sql import func
from app.core.database import Base

def generate_uuid():
    return str(uuid.uuid4())

class Company(Base):
    __tablename__ = "companies"

    id = Column(String, primary_key=True, default=generate_uuid)
    parent_company_id = Column(String, ForeignKey("companies.id"), nullable=True)
    name = Column(String, nullable=False)
    # Adicionado index=True para acelerar as buscas via URL
    slug = Column(String, unique=True, nullable=False, index=True) 
    cnpj = Column(String, nullable=False)
    service_type = Column(String, nullable=False)
    # Mudado para Boolean para maior clareza sem perder compatibilidade
    is_active = Column(Boolean, default=True) 
    created_at = Column(String, server_default=func.now())