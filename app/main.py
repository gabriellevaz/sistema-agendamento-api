from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import Base, engine

# Importando TODOS os nossos roteadores agora
from app.routers import companies, users, events, bookings, auth

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sistema de Agendamento Multi-Tenant",
    description="API para agendamento automatizado de consultas e aulas.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Conectando todas as rotas
app.include_router(companies.router)
app.include_router(users.router)
app.include_router(events.router)
app.include_router(bookings.router)
app.include_router(auth.router)


@app.get("/", tags=["Health Check"])
def read_root():
    return {"status": "online", "message": "Backend operando com sucesso."}