import uuid
from sqlalchemy import Column, String, ForeignKey, Index
from sqlalchemy.sql import func
from app.core.database import Base

def generate_uuid():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=generate_uuid)
    # Adicionado index=True para consultas rápidas de "listar usuários da empresa X"
    company_id = Column(String, ForeignKey("companies.id"), nullable=False, index=True) 
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True) # Index adicionado para login rápido
    password_hash = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    birth_date = Column(String, nullable=False)
    role = Column(String, nullable=False)
    created_at = Column(String, server_default=func.now())