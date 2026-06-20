from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.event import Event
from app.models.user import User
from app.schemas.event import EventCreate, EventResponse
from app.core.security import get_current_user # Importação crucial!

router = APIRouter(
    prefix="/events",
    tags=["Eventos e Serviços"]
)

@router.post("/", response_model=EventResponse)
def create_event(
    event_in: EventCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """
    Cria um novo serviço vinculado AUTOMATICAMENTE à empresa do admin logado.
    """
    # Criamos o evento injetando o company_id do usuário que está logado
    new_event = Event(
        **event_in.model_dump(), 
        company_id=current_user.company_id
    )
    
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    
    return new_event

@router.get("/", response_model=list[EventResponse])
def list_events(
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """
    Lista apenas os serviços pertencentes à empresa do usuário logado.
    Isso impede que uma empresa veja os serviços de outra.
    """
    return db.query(Event).filter(Event.company_id == current_user.company_id).all()