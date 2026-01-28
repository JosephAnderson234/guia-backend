from fastapi import APIRouter, HTTPException
from datetime import timedelta
# from fastapi import Depends
# from sqlalchemy.orm import Session
from app.schemas.cita import CitaRequest
# from app.db.session import get_db
# from app.db.models import Cita
from app.core.calendar import calendar_service
from app.core.config import CALENDAR_ID

router = APIRouter(prefix="/citas", tags=["Citas"])

@router.post("/agendar")
def crear_cita(cita: CitaRequest):
    # def crear_cita(cita: CitaRequest, db: Session = Depends(get_db)):


    try:
        event_ids = crear_eventos_google(cita)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail="Error al crear eventos en Google Calendar"
        )

    # nueva_cita = Cita(
    #     titulo=cita.titulo,
    #     descripcion=cita.descripcion,
    #     inicio=cita.inicio,
    #     fin=cita.fin,
    #     email=cita.email,
    #     google_event_id=event_id
    # )
    #
    # db.add(nueva_cita)
    # db.commit()
    # db.refresh(nueva_cita)

    return {
        "message": f"Citas creadas correctamente: {len(event_ids)} eventos",
        "google_event_ids": event_ids,
        "total_eventos": len(event_ids)
    }

@router.get("/test")
def test_endpoint():
    return {
  "cliente": "Juan Pérez",
  "fechas_iniciales": [
    "2026-01-28T10:00:00",
    "2026-01-29T14:30:00"
  ]
}

def crear_eventos_google(cita: CitaRequest) -> list[str]:
    """
    Crea eventos recurrentes en Google Calendar.
    Para cada fecha inicial seleccionada, crea un evento que se repite semanalmente 3 veces.
    Cada evento tiene una duración de 2 horas.
    Utiliza RRULE nativo de Google Calendar para optimizar las llamadas a la API.
    
    Returns:
        Lista de IDs de eventos recurrentes creados en Google Calendar
    """
    event_ids = []
    
    for fecha_inicial in cita.fechas_iniciales:
        evento = {
            "summary": f"Cita con {cita.cliente}",
            "description": "Cita agendada automáticamente - Se repite semanalmente 3 veces",
            "start": {
                "dateTime": fecha_inicial.isoformat(),
                "timeZone": "America/Lima"
            },
            "end": {
                "dateTime": (fecha_inicial + timedelta(hours=2)).isoformat(),
                "timeZone": "America/Lima"
            },
            "recurrence": ["RRULE:FREQ=WEEKLY;COUNT=3"]
        }
        
        evento_creado = calendar_service.events().insert(
            calendarId=CALENDAR_ID or "primary",
            body=evento,
            sendUpdates="all"
        ).execute()
        
        event_ids.append(evento_creado["id"])
    
    return event_ids
