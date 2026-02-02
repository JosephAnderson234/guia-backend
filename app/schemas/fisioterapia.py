"""
Esquemas Pydantic para Fisioterapia
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, date, time


# ==================== FISIOTERAPEUTA ====================

class FisioterapeutaBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100)


class FisioterapeutaCreate(FisioterapeutaBase):
    pass


class FisioterapeutaResponse(FisioterapeutaBase):
    id: int

    class Config:
        from_attributes = True


# ==================== MÁQUINA ====================

class MaquinaBase(BaseModel):
    codigo: str = Field(..., min_length=1, max_length=50)


class MaquinaCreate(MaquinaBase):
    pass


class MaquinaResponse(MaquinaBase):
    id: int

    class Config:
        from_attributes = True


# ==================== ESPACIO ====================

class EspacioBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100)


class EspacioCreate(EspacioBase):
    pass


class EspacioResponse(EspacioBase):
    id: int

    class Config:
        from_attributes = True


# ==================== BLOQUE HORARIO ====================

class BloqueHorarioBase(BaseModel):
    hora_inicio: time
    hora_fin: time


class BloqueHorarioCreate(BloqueHorarioBase):
    pass


class BloqueHorarioResponse(BloqueHorarioBase):
    id: int

    class Config:
        from_attributes = True


# ==================== PACIENTE ====================

class PacienteBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100)
    telefono: Optional[int] = None
    fecha_nacimiento: Optional[date] = None
    centro_terapia_id: Optional[int] = None
    usa_magneto: bool = False
    requiere_tratamiento_especial: bool = False
    seguro_medico: bool = False
    aseguradora: Optional[str] = None


class PacienteCreate(PacienteBase):
    pass


class PacienteResponse(PacienteBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ==================== DIAGNÓSTICO ====================

class DiagnosticoBase(BaseModel):
    paciente_id: int
    sessions: int = Field(..., gt=0)
    treatment: str = Field(..., min_length=1, max_length=255)


class DiagnosticoCreate(DiagnosticoBase):
    pass


class DiagnosticoResponse(DiagnosticoBase):
    id: int

    class Config:
        from_attributes = True


class DiagnosticoConPaciente(DiagnosticoResponse):
    paciente: Optional[PacienteResponse] = None


# ==================== RESERVA ====================

class ReservaBase(BaseModel):
    paciente_id: int
    fisioterapeuta_id: int
    espacio_id: int
    bloque_id: int
    maquina_id: Optional[int] = None
    fecha: date


class ReservaCreate(ReservaBase):
    pass


class ReservaResponse(ReservaBase):
    id: int

    class Config:
        from_attributes = True


class ReservaConDetalles(ReservaResponse):
    paciente: Optional[PacienteResponse] = None
    fisioterapeuta: Optional[FisioterapeutaResponse] = None
    espacio: Optional[EspacioResponse] = None
    bloque_horario: Optional[BloqueHorarioResponse] = None
    maquina: Optional[MaquinaResponse] = None


# ==================== CITA ====================

class CitaBase(BaseModel):
    titulo: str = Field(..., min_length=1, max_length=200)
    descripcion: Optional[str] = None
    email: Optional[str] = None
    google_event_id: str


class CitaCreate(CitaBase):
    inicio: datetime
    fin: datetime


class CitaResponse(CitaBase):
    id: int
    inicio: datetime
    fin: datetime
    fecha_creacion: datetime

    class Config:
        from_attributes = True


# ==================== DASHBOARDS ====================

class PacienteConHistorial(PacienteResponse):
    reservas: List[ReservaResponse] = []
    diagnosticos: List[DiagnosticoResponse] = []


class FisioterapeutaConAgenda(FisioterapeutaResponse):
    reservas: List[ReservaConDetalles] = []


# ==================== DISPONIBILIDAD ====================

class DisponibilidadQuery(BaseModel):
    """Query params para consultar disponibilidad"""
    fecha_inicio: date
    fecha_fin: date
    paciente_id: Optional[int] = None
    fisioterapeuta_id: Optional[int] = None


class BloqueDisponible(BaseModel):
    """Información de un bloque horario disponible"""
    fecha: date
    bloque_id: int
    hora_inicio: time
    hora_fin: time
    espacios_disponibles: int = Field(..., ge=0, le=9, description="Espacios libres (máximo 9)")
    maquinas_disponibles: Optional[int] = Field(None, ge=0, le=3, description="Máquinas libres (máximo 3)")

    class Config:
        from_attributes = True


class DisponibilidadResponse(BaseModel):
    """Respuesta con bloques disponibles"""
    bloques_disponibles: List[BloqueDisponible]
    total_bloques: int
    fecha_inicio: date
    fecha_fin: date


# ==================== TRATAMIENTO RECURRENTE ====================

class TratamientoCreate(BaseModel):
    """Request body para agendar tratamiento recurrente"""
    paciente_id: int = Field(..., gt=0, description="ID del paciente")
    fisioterapeuta_id: int = Field(..., gt=0, description="ID del fisioterapeuta")
    bloque_id: int = Field(..., gt=0, description="ID del bloque horario")
    fecha_inicio: date = Field(..., description="Fecha de inicio del tratamiento")
    total_sesiones: int = Field(..., gt=0, le=50, description="Total de sesiones a agendar (máx. 50)")
    requiere_maquina: bool = Field(default=False, description="Si el paciente requiere máquina")

    class Config:
        json_schema_extra = {
            "example": {
                "paciente_id": 1,
                "fisioterapeuta_id": 2,
                "bloque_id": 3,
                "fecha_inicio": "2026-02-10",
                "total_sesiones": 12,
                "requiere_maquina": True
            }
        }


class SesionAgendada(BaseModel):
    """Información de una sesión agendada"""
    id: int
    fecha: date
    bloque_id: int
    espacio_id: int
    maquina_id: Optional[int] = None
    hora_inicio: time
    hora_fin: time

    class Config:
        from_attributes = True


class TratamientoResponse(BaseModel):
    """Respuesta después de agendar un tratamiento"""
    paciente_id: int
    fisioterapeuta_id: int
    total_sesiones_agendadas: int
    sesiones: List[SesionAgendada]
    requiere_maquina: bool
    mensaje: str = Field(default="Tratamiento agendado exitosamente")

    class Config:
        json_schema_extra = {
            "example": {
                "paciente_id": 1,
                "fisioterapeuta_id": 2,
                "total_sesiones_agendadas": 12,
                "sesiones": [
                    {
                        "id": 101,
                        "fecha": "2026-02-10",
                        "bloque_id": 3,
                        "espacio_id": 5,
                        "maquina_id": 2,
                        "hora_inicio": "09:00:00",
                        "hora_fin": "09:40:00"
                    }
                ],
                "requiere_maquina": True,
                "mensaje": "Tratamiento agendado exitosamente"
            }
        }
