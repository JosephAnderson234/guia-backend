"""
Contenedor de Inyección de Dependencias (DI)
"""

from typing import Callable, Dict, Any
from sqlalchemy.orm import Session

from app.domain.ports import (
    PacienteRepository,
    ReservaRepository,
    DiagnosticoRepository,
    FisioterapeutaRepository,
    MaquinaRepository,
    EspacioRepository,
    BloqueHorarioRepository,
    CitaRepository
)
from app.domain.usecases import (
    CrearPaciente,
    ObtenerPaciente,
    ListarPacientes,
    ActualizarPaciente,
    EliminarPaciente,
    CrearReserva,
    ObtenerReserva,
    ListarReservasPaciente,
    ListarReservasFisioterapeuta,
    CrearDiagnostico,
    ObtenerDiagnosticoPaciente
)
from app.adapters.database.models import (
    PacienteRepositoryImpl
)


class Container:
    """
    Contenedor de Inyección de Dependencias (DI)
    Administra la creación y distribución de dependencias
    """
    
    def __init__(self, db: Session):
        self.db = db
        self._repositories: Dict[str, Any] = {}
        self._use_cases: Dict[str, Any] = {}
        self._initialize_repositories()
        self._initialize_use_cases()
    
    def _initialize_repositories(self):
        """Inicializar todos los repositorios"""
        self._repositories['paciente'] = PacienteRepositoryImpl(self.db)
        # Aquí irán los demás repositorios cuando se implementen
        # self._repositories['reserva'] = ReservaRepositoryImpl(self.db)
        # self._repositories['diagnostico'] = DiagnosticoRepositoryImpl(self.db)
        # self._repositories['fisioterapeuta'] = FisioterapeutaRepositoryImpl(self.db)
        # self._repositories['maquina'] = MaquinaRepositoryImpl(self.db)
        # self._repositories['espacio'] = EspacioRepositoryImpl(self.db)
        # self._repositories['bloque_horario'] = BloqueHorarioRepositoryImpl(self.db)
        # self._repositories['cita'] = CitaRepositoryImpl(self.db)
    
    def _initialize_use_cases(self):
        """Inicializar todos los casos de uso"""
        paciente_repo = self._repositories['paciente']
        
        self._use_cases['crear_paciente'] = CrearPaciente(paciente_repo)
        self._use_cases['obtener_paciente'] = ObtenerPaciente(paciente_repo)
        self._use_cases['listar_pacientes'] = ListarPacientes(paciente_repo)
        self._use_cases['actualizar_paciente'] = ActualizarPaciente(paciente_repo)
        self._use_cases['eliminar_paciente'] = EliminarPaciente(paciente_repo)
        
        # Aquí irán los demás casos de uso cuando se implementen los repositorios
        # reserva_repo = self._repositories.get('reserva')
        # if reserva_repo:
        #     self._use_cases['crear_reserva'] = CrearReserva(reserva_repo)
        #     self._use_cases['obtener_reserva'] = ObtenerReserva(reserva_repo)
        #     self._use_cases['listar_reservas_paciente'] = ListarReservasPaciente(reserva_repo)
        #     self._use_cases['listar_reservas_fisioterapeuta'] = ListarReservasFisioterapeuta(reserva_repo)
        
        # diagnostico_repo = self._repositories.get('diagnostico')
        # if diagnostico_repo:
        #     self._use_cases['crear_diagnostico'] = CrearDiagnostico(diagnostico_repo)
        #     self._use_cases['obtener_diagnostico_paciente'] = ObtenerDiagnosticoPaciente(diagnostico_repo)
    
    def get_repository(self, repo_type: str) -> Any:
        """Obtener un repositorio por tipo"""
        return self._repositories.get(repo_type)
    
    def get_use_case(self, use_case_name: str) -> Any:
        """Obtener un caso de uso por nombre"""
        return self._use_cases.get(use_case_name)
    
    def get_all_repositories(self) -> Dict[str, Any]:
        """Obtener todos los repositorios"""
        return self._repositories
    
    def get_all_use_cases(self) -> Dict[str, Any]:
        """Obtener todos los casos de uso"""
        return self._use_cases


# Instancia global del contenedor
_container: Container = None


def init_container(db: Session) -> Container:
    """Inicializar el contenedor de DI"""
    global _container
    _container = Container(db)
    return _container


def get_container() -> Container:
    """Obtener la instancia global del contenedor"""
    if _container is None:
        raise RuntimeError("Contenedor no inicializado. Llamar a init_container() primero.")
    return _container
