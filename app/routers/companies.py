from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.company import Company
from app.schemas.company import CompanyCreate, CompanyResponse

# Criamos o roteador para organizar as URLs
router = APIRouter(
    prefix="/companies",
    tags=["Empresas"]
)

@router.post("/", response_model=CompanyResponse)
def create_company(company_in: CompanyCreate, db: Session = Depends(get_db)):
    """
    Cria uma nova empresa no sistema.
    """
    # 1. Verifica se já existe uma empresa com esse 'slug' (URL)
    company_exists = db.query(Company).filter(Company.slug == company_in.slug).first()
    if company_exists:
        raise HTTPException(status_code=400, detail="Este slug já está em uso por outra empresa.")
    
    # 2. Converte os dados do Schema para o Model do SQLAlchemy
    new_company = Company(**company_in.model_dump())
    
    # 3. Salva no banco de dados
    db.add(new_company)
    db.commit()
    db.refresh(new_company) # Atualiza a variável com o ID gerado pelo banco
    
    return new_company

@router.get("/", response_model=list[CompanyResponse])
def list_companies(db: Session = Depends(get_db)):
    """
    Lista todas as empresas ativas no sistema.
    """
    return db.query(Company).all()