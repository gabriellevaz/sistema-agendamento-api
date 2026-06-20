# seed.py
from app.core.database import SessionLocal
from app.models.company import Company
from app.models.user import User
from app.core.security import get_password_hash

db = SessionLocal()

# 1. Cria a empresa de teste
clinica = Company(name="Clínica Exemplo", slug="clinica-exemplo", cnpj="00000000000191", service_type="medical")
db.add(clinica)
db.commit()

# 2. Cria um usuário admin para essa empresa
admin = User(
    company_id=clinica.id,
    name="Admin Teste",
    email="admin@clinica.com",
    password_hash=get_password_hash("123456"),
    birth_date="1990-01-01",
    role="admin"
)
db.add(admin)
db.commit()
print("Banco populado com sucesso!")