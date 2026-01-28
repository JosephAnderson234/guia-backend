"""
Capa de Dominio - Lógica de negocio pura, sin dependencias externas
"""

from .entities import *
from .ports import *
from .usecases import *

__all__ = [
    # Entities
    "Paciente",
    "Fisioterapeuta",
    "Maquina",
    "Espacio",
    "BloqueHorario",
    "Reserva",
    "Diagnostico",
    "Cita",
    # Ports
    "PacienteRepository",
    "FisioterapeutaRepository",
    "MaquinaRepository",
    "EspacioRepository",
    "BloqueHorarioRepository",
    "ReservaRepository",
    "DiagnosticoRepository",
    "CitaRepository",
    # Use Cases
    "CrearPaciente",
    "ObtenerPaciente",
    "ListarPacientes",
    "ActualizarPaciente",
    "EliminarPaciente",
    "CrearReserva",
    "ObtenerReserva",
    "ListarReservasPaciente",
    "ListarReservasFisioterapeuta",
    "CrearDiagnostico",
    "ObtenerDiagnosticoPaciente"
]
