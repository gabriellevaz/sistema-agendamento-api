from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.core.security import verify_password, create_access_token

router = APIRouter(
    tags=["Autenticação"]
)

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Autentica um usuário (via email e senha) e retorna o Token JWT.
    Nota: O OAuth2 usa 'username' por padrão, mas nós enviaremos o EMAIL neste campo.
    """
    # 1. Busca o usuário no banco pelo email (passado no campo username)
    user = db.query(User).filter(User.email == form_data.username).first()
    
    # 2. Verifica se o usuário existe e se a senha está correta
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 3. Gera o Token colocando o ID do usuário como 'sub' (subject)
    access_token = create_access_token(data={"sub": user.id})
    
    # 4. Retorna no formato exato que o protocolo OAuth2 exige
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "role": user.role # Extra para o Frontend saber o tipo de acesso
    }