"""
Rutas de Citas - Adaptador API Hexagonal
"""
from datetime import datetime, timedelta
from pydantic import BaseModel
from googleapiclient.errors import HttpError

from fastapi import APIRouter, HTTPException, Depends, Query
from datetime import date
from typing import Optional
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.fisioterapia import (
    DisponibilidadResponse,
    BloqueDisponible,
    TratamientoCreate,
    TratamientoResponse,
    SesionAgendada
)
from app.domain.usecases import ConsultarDisponibilidad, AgendarTratamientoRecurrente
from app.adapters.database.models import (
    PacienteRepositoryImpl,
    FisioterapeutaRepositoryImpl,
    EspacioRepositoryImpl,
    BloqueHorarioRepositoryImpl,
    MaquinaRepositoryImpl,
    ReservaRepositoryImpl
)

router = APIRouter(prefix="/api/citas", tags=["citas"])


# ==================== DEPENDENCY INJECTION ====================

def get_paciente_repo(db: Session = Depends(get_db)):
    return PacienteRepositoryImpl(db)


def get_fisioterapeuta_repo(db: Session = Depends(get_db)):
    return FisioterapeutaRepositoryImpl(db)


def get_espacio_repo(db: Session = Depends(get_db)):
    return EspacioRepositoryImpl(db)


def get_bloque_repo(db: Session = Depends(get_db)):
    return BloqueHorarioRepositoryImpl(db)


def get_maquina_repo(db: Session = Depends(get_db)):
    return MaquinaRepositoryImpl(db)


def get_reserva_repo(db: Session = Depends(get_db)):
    return ReservaRepositoryImpl(db)


# ==================== ENDPOINTS ====================

@router.get("/disponibles", response_model=DisponibilidadResponse)
async def consultar_disponibilidad(
    fecha_inicio: date = Query(..., description="Fecha inicial del rango de consulta"),
    fecha_fin: date = Query(..., description="Fecha final del rango de consulta"),
    paciente_id: Optional[int] = Query(None, description="ID del paciente (opcional)"),
    fisioterapeuta_id: Optional[int] = Query(None, description="ID del fisioterapeuta (opcional)"),
    espacio_repo = Depends(get_espacio_repo),
    bloque_repo = Depends(get_bloque_repo),
    fisio_repo = Depends(get_fisioterapeuta_repo),
    maquina_repo = Depends(get_maquina_repo),
    paciente_repo = Depends(get_paciente_repo)
) -> DisponibilidadResponse:
    """
    Consulta bloques horarios disponibles para un rango de fechas.
    
    **Validaciones:**
    - Espacios libres (máximo 9 espacios físicos)
    - Capacidad del fisioterapeuta (máximo 2 pacientes por bloque)
    - Restricción de trato especial (fisio solo puede atender 1 paciente si tiene trato especial)
    - Disponibilidad de máquinas (máximo 3 máquinas simultáneas)
    
    **Parámetros:**
    - **fecha_inicio**: Fecha inicial del rango
    - **fecha_fin**: Fecha final del rango
    - **paciente_id**: ID del paciente (opcional, para validar si requiere máquina)
    - **fisioterapeuta_id**: ID del fisioterapeuta (opcional, para filtrar su disponibilidad)
    
    **Retorna:**
    Lista de bloques disponibles con información de espacios y máquinas disponibles.
    """
    try:
        # Validar que fecha_fin >= fecha_inicio
        if fecha_fin < fecha_inicio:
            raise HTTPException(
                status_code=400,
                detail="La fecha_fin debe ser mayor o igual a fecha_inicio"
            )
        
        # Ejecutar caso de uso
        use_case = ConsultarDisponibilidad(
            espacio_repo=espacio_repo,
            bloque_repo=bloque_repo,
            fisio_repo=fisio_repo,
            maquina_repo=maquina_repo,
            paciente_repo=paciente_repo
        )
        
        bloques_data = await use_case.ejecutar(
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            paciente_id=paciente_id,
            fisioterapeuta_id=fisioterapeuta_id
        )
        
        # Convertir a schemas
        bloques = [BloqueDisponible(**bloque) for bloque in bloques_data]
        
        return DisponibilidadResponse(
            bloques_disponibles=bloques,
            total_bloques=len(bloques),
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin
        )
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al consultar disponibilidad: {str(e)}"
        )


@router.post("/agendar", response_model=TratamientoResponse)
async def agendar_tratamiento(
    tratamiento: TratamientoCreate,
    db: Session = Depends(get_db),
    paciente_repo = Depends(get_paciente_repo),
    fisio_repo = Depends(get_fisioterapeuta_repo),
    espacio_repo = Depends(get_espacio_repo),
    bloque_repo = Depends(get_bloque_repo),
    maquina_repo = Depends(get_maquina_repo),
    reserva_repo = Depends(get_reserva_repo)
) -> TratamientoResponse:
    """
    Agenda un tratamiento recurrente semanal.
    
    **Reglas de Negocio:**
    1. Sesiones de 40 minutos en bloques fijos
    2. Solo 1 paciente por espacio y bloque (máximo 9 espacios)
    3. Fisioterapeuta puede atender máximo 2 pacientes por bloque
    4. Si paciente tiene trato especial, fisio SOLO lo atiende a él
    5. Si paciente requiere máquina, debe usarse en TODAS las sesiones
    6. Máximo 3 máquinas simultáneas por bloque
    7. Máximo 3 sesiones por semana
    8. Sesiones siempre el mismo día de la semana y mismo bloque
    
    **Request Body:**
    ```json
    {
      "paciente_id": 1,
      "fisioterapeuta_id": 2,
      "bloque_id": 3,
      "fecha_inicio": "2026-02-10",
      "total_sesiones": 12,
      "requiere_maquina": true
    }
    ```
    
    **Validaciones:**
    - Valida TODAS las reglas antes de insertar
    - Usa transacciones SQL (rollback automático si falla)
    - Si alguna sesión no puede agendarse, aborta toda la operación
    
    **Retorna:**
    Lista de sesiones agendadas con detalles (fecha, espacio, máquina, horario).
    """
    try:
        # Ejecutar caso de uso con transacción
        use_case = AgendarTratamientoRecurrente(
            db=db,
            paciente_repo=paciente_repo,
            fisio_repo=fisio_repo,
            espacio_repo=espacio_repo,
            bloque_repo=bloque_repo,
            maquina_repo=maquina_repo,
            reserva_repo=reserva_repo
        )
        
        reservas = await use_case.ejecutar(
            paciente_id=tratamiento.paciente_id,
            fisioterapeuta_id=tratamiento.fisioterapeuta_id,
            bloque_id=tratamiento.bloque_id,
            fecha_inicio=tratamiento.fecha_inicio,
            total_sesiones=tratamiento.total_sesiones,
            requiere_maquina=tratamiento.requiere_maquina
        )
        
        # Obtener información de bloques horarios para las respuestas
        bloques_info = {}
        for reserva in reservas:
            if reserva.bloque_id not in bloques_info:
                bloque = await bloque_repo.obtener_por_id(reserva.bloque_id)
                if bloque:
                    bloques_info[reserva.bloque_id] = {
                        "hora_inicio": bloque.hora_inicio,
                        "hora_fin": bloque.hora_fin
                    }
        
        # Convertir a schemas de respuesta
        sesiones = [
            SesionAgendada(
                id=reserva.id,
                fecha=reserva.fecha,
                bloque_id=reserva.bloque_id,
                espacio_id=reserva.espacio_id,
                maquina_id=reserva.maquina_id,
                hora_inicio=bloques_info.get(reserva.bloque_id, {}).get("hora_inicio"),
                hora_fin=bloques_info.get(reserva.bloque_id, {}).get("hora_fin")
            )
            for reserva in reservas
        ]
        
        return TratamientoResponse(
            paciente_id=tratamiento.paciente_id,
            fisioterapeuta_id=tratamiento.fisioterapeuta_id,
            total_sesiones_agendadas=len(sesiones),
            sesiones=sesiones,
            requiere_maquina=tratamiento.requiere_maquina,
            mensaje=f"Tratamiento agendado exitosamente: {len(sesiones)} sesiones creadas"
        )
    
    except ValueError as e:
        # Errores de validación de negocio
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Errores inesperados
        raise HTTPException(
            status_code=500,
            detail=f"Error al agendar tratamiento: {str(e)}"
        )

class CitaRequest(BaseModel):
    """DTO para crear citas"""
    cliente: str
    fechas_iniciales: list[datetime]


class CitaResponse(BaseModel):
    """DTO de respuesta de citas"""
    message: str
    google_event_ids: list[str]
    total_eventos: int
    
@router.post("/google/agendar", response_model=CitaResponse)
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