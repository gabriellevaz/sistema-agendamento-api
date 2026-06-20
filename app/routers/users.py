from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.core.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.core.security import oauth2_scheme

# Configuração do encriptador de senhas (usando o algoritmo bcrypt)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

router = APIRouter(
    prefix="/users",
    tags=["Usuários"]
)

@router.post("/", response_model=UserResponse)
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    """
    Cria um novo usuário (Cliente, Admin ou Médico).
    """
    # 1. Verifica se o email já existe
    user_exists = db.query(User).filter(User.email == user_in.email).first()
    if user_exists:
        raise HTTPException(status_code=400, detail="Este email já está cadastrado.")
    
    # 2. Separa os dados e troca a senha pura pelo Hash
    user_data = user_in.model_dump()
    raw_password = user_data.pop("password") # Remove a senha pura do dicionário
    hashed_password = get_password_hash(raw_password) # Gera o hash
    
    # 3. Cria o objeto do SQLAlchemy
    new_user = User(**user_data, password_hash=hashed_password)
    
    # 4. Salva no banco
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

@router.get("/", response_model=list[UserResponse])
def list_users(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)): # <--- Adicionamos o token aqui
    """
    Lista todos os usuários (Agora protegida por Token!).
    """
    return db.query(User).all()