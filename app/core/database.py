from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Nome do arquivo do banco local que será criado automaticamente
SQLALCHEMY_DATABASE_URL = "sqlite:///./agendamento.db"

# Engine de conexão do SQLite
engine = create_engine(
    # check_same_thread=False é obrigatório apenas para o SQLite
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Fábrica de sessões com o banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Classe base que nossos modelos do banco irão herdar
Base = declarative_base()

# Dependency Injection para os endpoints do FastAPI utilizarem o banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()