from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.company import Company
from app.schemas.company import CompanyCreate, CompanyResponse
# Se você tiver um decorador de autenticação para Super Admin, importe aqui:
# from app.core.security import get_current_user 

router = APIRouter(
    prefix="/companies",
    tags=["Empresas"]
)

@router.post("/", response_model=CompanyResponse)
def create_company(company_in: CompanyCreate, db: Session = Depends(get_db)):
    """
    Cria uma nova empresa no sistema.
    """
    # 1. Verifica se já existe uma empresa com esse 'slug' para evitar conflitos de URL
    company_exists = db.query(Company).filter(Company.slug == company_in.slug).first()
    if company_exists:
        raise HTTPException(status_code=400, detail="Este slug já está em uso por outra empresa.")
    
    # 2. Converte os dados do Schema para o Model do SQLAlchemy
    new_company = Company(**company_in.model_dump())
    
    # 3. Salva no banco de dados
    db.add(new_company)
    db.commit()
    db.refresh(new_company)
    
    return new_company

@router.get("/by-slug/{slug}", response_model=CompanyResponse)
def get_company_by_slug(slug: str, db: Session = Depends(get_db)):
    """
    Busca os dados da empresa pelo slug.
    Esta rota é pública para permitir que o Frontend identifique a empresa antes do login.
    """
    company = db.query(Company).filter(Company.slug == slug).first()
    if not company:
        raise HTTPException(status_code=404, detail="Empresa não encontrada.")
    
    # Verifica se a empresa está ativa antes de permitir o acesso
    if not company.is_active:
        raise HTTPException(status_code=403, detail="Esta empresa está temporariamente inativa.")
        
    return company

@router.get("/", response_model=list[CompanyResponse])
def list_companies(db: Session = Depends(get_db)):
    """
    Lista todas as empresas. 
    RECOMENDAÇÃO: Em produção, proteja esta rota para que apenas 
    VOCÊ (o dono do sistema) consiga listar todos os clientes.
    """
    return db.query(Company).all()