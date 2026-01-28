"""
Entidades de Dominio - Lógica de negocio pura sin dependencias externas
"""

from dataclasses import dataclass, field
from datetime import datetime, date, time
from typing import Optional, List


@dataclass
class Paciente:
    """Entidad de dominio: Paciente"""
    id: Optional[int] = None
    nombre: str = ""
    telefono: Optional[int] = None
    fecha_nacimiento: Optional[date] = None
    centro_terapia_id: Optional[int] = None
    usa_magneto: bool = False
    requiere_tratamiento_especial: bool = False
    seguro_medico: bool = False
    aseguradora: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    
    # Relaciones
    reservas: List['Reserva'] = field(default_factory=list)
    diagnosticos: List['Diagnostico'] = field(default_factory=list)


@dataclass
class Fisioterapeuta:
    """Entidad de dominio: Fisioterapeuta"""
    id: Optional[int] = None
    nombre: str = ""
    
    reservas: List['Reserva'] = field(default_factory=list)


@dataclass
class Maquina:
    """Entidad de dominio: Máquina"""
    id: Optional[int] = None
    codigo: str = ""
    
    reservas: List['Reserva'] = field(default_factory=list)


@dataclass
class Espacio:
    """Entidad de dominio: Espacio de Terapia"""
    id: Optional[int] = None
    nombre: str = ""
    
    reservas: List['Reserva'] = field(default_factory=list)


@dataclass
class BloqueHorario:
    """Entidad de dominio: Bloque Horario"""
    id: Optional[int] = None
    hora_inicio: time = field(default_factory=lambda: time(0, 0))
    hora_fin: time = field(default_factory=lambda: time(1, 0))
    
    reservas: List['Reserva'] = field(default_factory=list)


@dataclass
class Reserva:
    """Entidad de dominio: Reserva de Cita"""
    id: Optional[int] = None
    paciente_id: int = 0
    fisioterapeuta_id: int = 0
    espacio_id: int = 0
    bloque_id: int = 0
    maquina_id: Optional[int] = None
    fecha: date = field(default_factory=date.today)
    
    # Relaciones
    paciente: Optional[Paciente] = None
    fisioterapeuta: Optional[Fisioterapeuta] = None
    espacio: Optional[Espacio] = None
    bloque_horario: Optional[BloqueHorario] = None
    maquina: Optional[Maquina] = None


@dataclass
class Diagnostico:
    """Entidad de dominio: Diagnóstico"""
    id: Optional[int] = None
    paciente_id: int = 0
    sessions: int = 0
    treatment: str = ""
    
    # Relaciones
    paciente: Optional[Paciente] = None


@dataclass
class Cita:
    """Entidad de dominio: Cita con Google Calendar"""
    id: Optional[int] = None
    titulo: str = ""
    descripcion: Optional[str] = None
    inicio: datetime = field(default_factory=datetime.utcnow)
    fin: datetime = field(default_factory=datetime.utcnow)
    email: Optional[str] = None
    google_event_id: str = ""
    fecha_creacion: datetime = field(default_factory=datetime.utcnow)
