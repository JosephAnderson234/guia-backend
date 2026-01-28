"""
Esquemas Pydantic - DTOs para entrada/salida de API
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
