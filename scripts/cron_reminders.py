import os
import sys
from datetime import datetime, timedelta

# --- TRUQUE DE ARQUITETURA: AJUSTE DE CAMINHO ---
# Descobre a pasta raiz do projeto e avisa o Python que ele pode importar a pasta 'app'
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

# Agora as importações do nosso projeto funcionam perfeitamente!
from app.core.database import SessionLocal
from app.models.booking import Booking
from app.models.user import User
from app.models.event import Event
from app.models.company import Company

def mock_send_email(to_email: str, subject: str, body: str):
    """
    Função temporária para simular o envio de e-mail no console.
    Mais para a frente, podemos plugar um serviço real aqui (como SendGrid, Mailgun ou SMTP).
    """
    print("\n" + "="*50)
    print(f"📧 DISPARANDO E-MAIL PARA: {to_email}")
    print(f"📝 ASSUNTO: {subject}")
    print(f"💬 CORPO:\n{body}")
    print("="*50)

def check_and_send_reminders():
    # Abre uma conexão dedicada com o SQLite para este processamento
    db = SessionLocal()
    
    try:
        now = datetime.now()
        print(f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] Iniciando checagem de lembretes...")
        
        # 1. Busca todos os agendamentos confirmados
        bookings = db.query(Booking).filter(Booking.status == "confirmed").all()
        
        for booking in bookings:
            # Converte a string de data do banco para um objeto datetime do Python
            # Ex de formato salvo: "2026-06-25T14:00:00"
            event_time = datetime.fromisoformat(booking.scheduled_time)
            
            # Calcula a diferença de tempo entre o evento e o momento atual
            time_delta = event_time - now
            
            # Busca o cliente e o evento correspondente para colocar as informações no e-mail
            customer = db.query(User).filter(User.id == booking.customer_id).first()
            event = db.query(Event).filter(Event.id == booking.event_id).first()
            
            if not customer or not event:
                continue
                
            # --- LÓGICA DO LEMBRETE DE 48 HORAS ---
            # Se o evento acontecer entre 24h e 48h a partir de agora, e o lembrete de 48h NÃO foi enviado
            if timedelta(hours=24) < time_delta <= timedelta(hours=48) and booking.reminder_48h_sent == 0:
                subject = f"Lembrete de Agendamento: {event.title} em 48 horas"
                body = (
                    f"Olá, {customer.name}!\n\n"
                    f"Este é um lembrete de que sua consulta/aula de '{event.title}' está chegando.\n"
                    f"📅 Data/Hora: {event_time.strftime('%d/%m/%Y às %H:%M')}\n\n"
                    f"Seu QR Code de comparecimento é: {booking.qr_code_token}\n"
                    f"Caso precise cancelar, acesse o sistema com antecedência."
                )
                mock_send_email(customer.email, subject, body)
                
                # Atualiza a flag no banco para nunca mais enviar este lembrete para este agendamento
                booking.reminder_48h_sent = 1
                db.commit()

            # --- LÓGICA DO LEMBRETE DE 24 HORAS ---
            # Se o evento acontecer entre 0h e 24h a partir de agora, e o lembrete de 24h NÃO foi enviado
            elif timedelta(hours=0) < time_delta <= timedelta(hours=24) and booking.reminder_24h_sent == 0:
                subject = f"🚨 Atenção: Seu agendamento de {event.title} é AMANHÃ"
                body = (
                    f"Olá, {customer.name}!\n\n"
                    f"Faltam menos de 24 horas para o seu compromisso de '{event.title}'.\n"
                    f"📅 Data/Hora: {event_time.strftime('%d/%m/%Y às %H:%M')}\n\n"
                    f"Apresente este token ou QR Code na recepção: {booking.qr_code_token}"
                )
                mock_send_email(customer.email, subject, body)
                
                # Prontinho, flag de 24h selada
                booking.reminder_24h_sent = 1
                db.commit()
                
        print("Checagem finalizada com sucesso.")
        
    except Exception as e:
        print(f"❌ Erro durante a execução do robô: {str(e)}")
        db.rollback()
    finally:
        # Fecha a conexão com o banco de dados obrigatoriamente
        db.close()

if __name__ == "__main__":
    check_and_send_reminders()