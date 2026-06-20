import uuid
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base

def generate_uuid():
    return str(uuid.uuid4())

class Company(Base):
    __tablename__ = "companies"

    id = Column(String, primary_key=True, default=generate_uuid)
    parent_company_id = Column(String, ForeignKey("companies.id"), nullable=True)
    name = Column(String, nullable=False)
    slug = Column(String, unique=True, nullable=False)
    cnpj = Column(String, nullable=False)
    service_type = Column(String, nullable=False)
    is_active = Column(Integer, default=1) # 1 = Ativa, 0 = Inativa
    created_at = Column(String, server_default=func.now())