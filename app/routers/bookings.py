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
    """
    Realiza um novo agendamento, garantindo que o horário não conflite.
    O customer_id é injetado automaticamente através do usuário logado no Token.
    """
    # Geramos um token único para o futuro QR Code
    qr_token = f"QR-{uuid.uuid4().hex[:10].upper()}"
    
    # Pegamos os dados que vieram do Frontend/Swagger e forçamos o customer_id
    # a ser o ID da pessoa que está logada, garantindo segurança.
    booking_data = booking_in.model_dump()
    booking_data["customer_id"] = current_user.id 
    
    new_booking = Booking(
        **booking_data,
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
    """
    Lista todos os agendamentos.
    Regra: Clientes comuns veem apenas a sua própria agenda. Admins/Staff veem tudo.
    """
    if current_user.role == "customer":
        # Retorna apenas os agendamentos onde o dono é o usuário logado
        return db.query(Booking).filter(Booking.customer_id == current_user.id).all()
    
    # Se passou do 'if' acima, é porque tem cargo elevado, então retorna todos
    return db.query(Booking).all()