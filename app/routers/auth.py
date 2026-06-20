from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.models.company import Company
from app.core.security import verify_password, create_access_token

router = APIRouter(
    tags=["Autenticação"]
)

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Autentica o usuário e garante que a empresa vinculada esteja ativa.
    """
    # 1. Busca o usuário pelo email
    user = db.query(User).filter(User.email == form_data.username).first()
    
    # 2. Verifica existência e senha
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 3. VERIFICAÇÃO MULTI-TENANT: A empresa deste usuário está ativa?
    company = db.query(Company).filter(Company.id == user.company_id).first()
    if not company or not company.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso bloqueado: Esta conta de empresa está inativa."
        )
    
    # 4. Gera o Token
    # DICA: Adicionamos o company_id no token para facilitar as próximas consultas!
    access_token = create_access_token(data={"sub": user.id, "company_id": user.company_id})
    
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "role": user.role,
        "company_slug": company.slug # Útil para o front redirecionar corretamente
    }