"""
Rutas de Citas - Adaptador API Hexagonal
"""

from fastapi import APIRouter, HTTPException
from datetime import datetime, timedelta
from pydantic import BaseModel
from googleapiclient.errors import HttpError

router = APIRouter(prefix="/api/citas", tags=["citas"])


class CitaRequest(BaseModel):
    """DTO para crear citas"""
    cliente: str
    fechas_iniciales: list[datetime]


class CitaResponse(BaseModel):
    """DTO de respuesta de citas"""
    message: str
    google_event_ids: list[str]
    total_eventos: int


@router.post("/agendar", response_model=CitaResponse)
async def agendar_citas(cita: CitaRequest) -> CitaResponse:
    """Agendar citas con Google Calendar"""
    try:
        from app.adapters.external.google_calendar import calendar_service, CALENDAR_ID
        
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
        
        return CitaResponse(
            message=f"Citas creadas correctamente: {len(event_ids)} eventos",
            google_event_ids=event_ids,
            total_eventos=len(event_ids)
        )
    except HttpError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error al crear eventos en Google Calendar: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error interno: {str(e)}"
        )


@router.get("/test")
async def test_endpoint():
    """Endpoint de prueba"""
    return {
        "cliente": "Juan Pérez",
        "fechas_iniciales": [
            "2026-01-28T10:00:00",
            "2026-01-29T14:30:00"
        ]
    }
