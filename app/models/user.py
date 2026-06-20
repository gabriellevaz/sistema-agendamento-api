import uuid
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base

def generate_uuid():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=generate_uuid)
    company_id = Column(String, ForeignKey("companies.id"), nullable=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    birth_date = Column(String, nullable=False) # Formato: YYYY-MM-DD
    role = Column(String, nullable=False) # 'customer', 'admin', 'doctor', 'staff'
    created_at = Column(String, server_default=func.now())