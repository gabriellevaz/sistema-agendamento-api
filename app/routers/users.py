from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.core.database import get_db
from app.models.user import User
from app.models.company import Company # Importante para validar o slug
from app.schemas.user import UserCreate, UserResponse
from app.core.security import get_current_user # Agora usamos o user completo, não só o token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

router = APIRouter(
    prefix="/users",
    tags=["Usuários"]
)

@router.post("/register/{company_slug}", response_model=UserResponse)
def register_user(company_slug: str, user_in: UserCreate, db: Session = Depends(get_db)):
    """
    Registra um usuário vinculado à empresa específica via slug.
    Ex: /users/register/clinica-silva
    """
    # 1. Busca a empresa pelo slug
    company = db.query(Company).filter(Company.slug == company_slug).first()
    if not company or not company.is_active == 0:
        raise HTTPException(status_code=404, detail="Empresa não encontrada ou inativa.")
    
    # 2. Verifica duplicidade de email
    if db.query(User).filter(User.email == user_in.email).first():
        raise HTTPException(status_code=400, detail="Este email já está cadastrado.")
    
    # 3. Cria o usuário com o company_id da empresa encontrada
    user_data = user_in.model_dump()
    raw_password = user_data.pop("password")
    
    new_user = User(
        **user_data, 
        password_hash=get_password_hash(raw_password),
        company_id=company.id  # <--- INJEÇÃO DE SEGURANÇA
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/", response_model=list[UserResponse])
def list_users(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Lista apenas os usuários que pertencem à mesma empresa do admin logado.
    """
    if current_user.role not in ["admin", "staff"]:
        raise HTTPException(status_code=403, detail="Acesso não autorizado.")
        
    return db.query(User).filter(User.company_id == current_user.company_id).all()