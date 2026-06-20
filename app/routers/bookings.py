import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.core.database import get_db
from app.models.booking import Booking
from app.schemas.booking import BookingCreate, BookingResponse

# Importamos a nossa nova função de segurança que lê o Token
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/bookings",
    tags=["Agendamentos"]
)

    @router.post("/", response_model=BookingResponse)
    def create_booking(booking_in: BookingCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
        # 1. Garante que o agendamento seja sempre vinculado à empresa do usuário
        qr_token = f"QR-{uuid.uuid4().hex[:10].upper()}"
        
        new_booking = Booking(
            company_id=current_user.company_id, # <--- SEGURANÇA: Vincula à empresa do usuário
            customer_id=current_user.id,
            event_id=booking_in.event_id,
            scheduled_time=booking_in.scheduled_time,
            qr_code_token=qr_token
        )
    
    
    try:
        db.add(new_booking)
        db.commit()
        db.refresh(new_booking)
        return new_booking
        
    except IntegrityError:
        # Se o SQLite barrar por causa do nosso Índice Único (horário já ocupado)
        db.rollback()
        raise HTTPException(
            status_code=409, 
            detail="Este horário acabou de ser reservado por outra pessoa. Escolha outro horário."
        )

    @router.get("/", response_model=list[BookingResponse])
    def list_bookings(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
        # 1. Filtro Global: Ninguém vê dados de outra empresa
        query = db.query(Booking).filter(Booking.company_id == current_user.company_id)
        
        # 2. Se for cliente comum, restringe ainda mais (apenas os dele)
        if current_user.role == "customer":
            query = query.filter(Booking.customer_id == current_user.id)
        
        return query.all()