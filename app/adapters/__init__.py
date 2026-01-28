"""
Capa de Adaptadores - Implementaciones concretas de los puertos
"""

from .database.models import (
    PacienteRepositoryImpl,
    FisioterapeutaORM,
    MaquinaORM,
    EspacioORM,
    BloqueHorarioORM,
    PacienteORM,
    ReservaORM,
    DiagnosticoORM,
    CitaORM
)

__all__ = [
    "PacienteRepositoryImpl",
    "FisioterapeutaORM",
    "MaquinaORM",
    "EspacioORM",
    "BloqueHorarioORM",
    "PacienteORM",
    "ReservaORM",
    "DiagnosticoORM",
    "CitaORM"
]
