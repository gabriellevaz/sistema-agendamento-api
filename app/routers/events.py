from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.event import Event
from app.schemas.event import EventCreate, EventResponse
from app.core.security import oauth2_scheme

router = APIRouter(
    prefix="/events",
    tags=["Eventos e Serviços"]
)

@router.post("/", response_model=EventResponse)
def create_event(event_in: EventCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    Cria um novo serviço (ex: Consulta de Pediatria).
    """
    new_event = Event(**event_in.model_dump())
    
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    
    return new_event

@router.get("/", response_model=list[EventResponse])
def list_events(db: Session = Depends(get_db)):
    """
    Lista todos os serviços disponíveis.
    """
    return db.query(Event).all()