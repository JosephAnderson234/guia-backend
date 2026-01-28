"""
Puertos (Interfaces) - Contratos para los adaptadores
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities import (
    Paciente, Fisioterapeuta, Maquina, Espacio, 
    BloqueHorario, Reserva, Diagnostico, Cita
)


class PacienteRepository(ABC):
    """Puerto: Repositorio de Pacientes"""
    
    @abstractmethod
    async def crear(self, paciente: Paciente) -> Paciente:
        pass
    
    @abstractmethod
    async def obtener_por_id(self, paciente_id: int) -> Optional[Paciente]:
        pass
    
    @abstractmethod
    async def listar(self, skip: int = 0, limit: int = 10) -> List[Paciente]:
        pass
    
    @abstractmethod
    async def actualizar(self, paciente_id: int, datos: dict) -> Paciente:
        pass
    
    @abstractmethod
    async def eliminar(self, paciente_id: int) -> bool:
        pass


class ReservaRepository(ABC):
    """Puerto: Repositorio de Reservas"""
    
    @abstractmethod
    async def crear(self, reserva: Reserva) -> Reserva:
        pass
    
    @abstractmethod
    async def obtener_por_id(self, reserva_id: int) -> Optional[Reserva]:
        pass
    
    @abstractmethod
    async def listar(self, skip: int = 0, limit: int = 10) -> List[Reserva]:
        pass
    
    @abstractmethod
    async def listar_por_paciente(self, paciente_id: int) -> List[Reserva]:
        pass
    
    @abstractmethod
    async def listar_por_fisioterapeuta(self, fisioterapeuta_id: int) -> List[Reserva]:
        pass
    
    @abstractmethod
    async def actualizar(self, reserva_id: int, datos: dict) -> Reserva:
        pass
    
    @abstractmethod
    async def eliminar(self, reserva_id: int) -> bool:
        pass


class DiagnosticoRepository(ABC):
    """Puerto: Repositorio de Diagnósticos"""
    
    @abstractmethod
    async def crear(self, diagnostico: Diagnostico) -> Diagnostico:
        pass
    
    @abstractmethod
    async def obtener_por_id(self, diagnostico_id: int) -> Optional[Diagnostico]:
        pass
    
    @abstractmethod
    async def listar_por_paciente(self, paciente_id: int) -> List[Diagnostico]:
        pass


class FisioterapeutaRepository(ABC):
    """Puerto: Repositorio de Fisioterapeutas"""
    
    @abstractmethod
    async def crear(self, fisioterapeuta: Fisioterapeuta) -> Fisioterapeuta:
        pass
    
    @abstractmethod
    async def obtener_por_id(self, fisioterapeuta_id: int) -> Optional[Fisioterapeuta]:
        pass
    
    @abstractmethod
    async def listar(self) -> List[Fisioterapeuta]:
        pass


class MaquinaRepository(ABC):
    """Puerto: Repositorio de Máquinas"""
    
    @abstractmethod
    async def crear(self, maquina: Maquina) -> Maquina:
        pass
    
    @abstractmethod
    async def obtener_por_id(self, maquina_id: int) -> Optional[Maquina]:
        pass
    
    @abstractmethod
    async def listar(self) -> List[Maquina]:
        pass


class EspacioRepository(ABC):
    """Puerto: Repositorio de Espacios"""
    
    @abstractmethod
    async def crear(self, espacio: Espacio) -> Espacio:
        pass
    
    @abstractmethod
    async def obtener_por_id(self, espacio_id: int) -> Optional[Espacio]:
        pass
    
    @abstractmethod
    async def listar(self) -> List[Espacio]:
        pass


class BloqueHorarioRepository(ABC):
    """Puerto: Repositorio de Bloques Horarios"""
    
    @abstractmethod
    async def crear(self, bloque: BloqueHorario) -> BloqueHorario:
        pass
    
    @abstractmethod
    async def obtener_por_id(self, bloque_id: int) -> Optional[BloqueHorario]:
        pass
    
    @abstractmethod
    async def listar(self) -> List[BloqueHorario]:
        pass


class CitaRepository(ABC):
    """Puerto: Repositorio de Citas"""
    
    @abstractmethod
    async def crear(self, cita: Cita) -> Cita:
        pass
    
    @abstractmethod
    async def obtener_por_id(self, cita_id: int) -> Optional[Cita]:
        pass
    
    @abstractmethod
    async def listar(self) -> List[Cita]:
        pass
