"""
Casos de Uso - Lógica de aplicación
"""

from typing import List, Optional
from app.domain.entities import Paciente, Reserva, Diagnostico
from app.domain.ports import PacienteRepository, ReservaRepository, DiagnosticoRepository


class CrearPaciente:
    """Caso de uso: Crear un paciente"""
    
    def __init__(self, paciente_repo: PacienteRepository):
        self.paciente_repo = paciente_repo
    
    async def ejecutar(self, datos: dict) -> Paciente:
        paciente = Paciente(**datos)
        return await self.paciente_repo.crear(paciente)


class ObtenerPaciente:
    """Caso de uso: Obtener un paciente por ID"""
    
    def __init__(self, paciente_repo: PacienteRepository):
        self.paciente_repo = paciente_repo
    
    async def ejecutar(self, paciente_id: int) -> Optional[Paciente]:
        return await self.paciente_repo.obtener_por_id(paciente_id)


class ListarPacientes:
    """Caso de uso: Listar pacientes"""
    
    def __init__(self, paciente_repo: PacienteRepository):
        self.paciente_repo = paciente_repo
    
    async def ejecutar(self, skip: int = 0, limit: int = 10) -> List[Paciente]:
        return await self.paciente_repo.listar(skip, limit)


class ActualizarPaciente:
    """Caso de uso: Actualizar un paciente"""
    
    def __init__(self, paciente_repo: PacienteRepository):
        self.paciente_repo = paciente_repo
    
    async def ejecutar(self, paciente_id: int, datos: dict) -> Paciente:
        return await self.paciente_repo.actualizar(paciente_id, datos)


class EliminarPaciente:
    """Caso de uso: Eliminar un paciente"""
    
    def __init__(self, paciente_repo: PacienteRepository):
        self.paciente_repo = paciente_repo
    
    async def ejecutar(self, paciente_id: int) -> bool:
        return await self.paciente_repo.eliminar(paciente_id)


class CrearReserva:
    """Caso de uso: Crear una reserva"""
    
    def __init__(self, reserva_repo: ReservaRepository):
        self.reserva_repo = reserva_repo
    
    async def ejecutar(self, datos: dict) -> Reserva:
        reserva = Reserva(**datos)
        return await self.reserva_repo.crear(reserva)


class ObtenerReserva:
    """Caso de uso: Obtener una reserva"""
    
    def __init__(self, reserva_repo: ReservaRepository):
        self.reserva_repo = reserva_repo
    
    async def ejecutar(self, reserva_id: int) -> Optional[Reserva]:
        return await self.reserva_repo.obtener_por_id(reserva_id)


class ListarReservasPaciente:
    """Caso de uso: Listar reservas de un paciente"""
    
    def __init__(self, reserva_repo: ReservaRepository):
        self.reserva_repo = reserva_repo
    
    async def ejecutar(self, paciente_id: int) -> List[Reserva]:
        return await self.reserva_repo.listar_por_paciente(paciente_id)


class ListarReservasFisioterapeuta:
    """Caso de uso: Listar reservas de un fisioterapeuta"""
    
    def __init__(self, reserva_repo: ReservaRepository):
        self.reserva_repo = reserva_repo
    
    async def ejecutar(self, fisioterapeuta_id: int) -> List[Reserva]:
        return await self.reserva_repo.listar_por_fisioterapeuta(fisioterapeuta_id)


class CrearDiagnostico:
    """Caso de uso: Crear un diagnóstico"""
    
    def __init__(self, diagnostico_repo: DiagnosticoRepository):
        self.diagnostico_repo = diagnostico_repo
    
    async def ejecutar(self, datos: dict) -> Diagnostico:
        diagnostico = Diagnostico(**datos)
        return await self.diagnostico_repo.crear(diagnostico)


class ObtenerDiagnosticoPaciente:
    """Caso de uso: Obtener diagnósticos de un paciente"""
    
    def __init__(self, diagnostico_repo: DiagnosticoRepository):
        self.diagnostico_repo = diagnostico_repo
    
    async def ejecutar(self, paciente_id: int) -> List[Diagnostico]:
        return await self.diagnostico_repo.listar_por_paciente(paciente_id)
