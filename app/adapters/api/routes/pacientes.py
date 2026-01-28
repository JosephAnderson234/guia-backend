"""
Rutas de API Hexagonal - Pacientes
"""

from fastapi import APIRouter, Depends, HTTPException
from typing import List

from app.shared.schemas import PacienteCreate, PacienteResponse, PacienteConHistorial
from app.domain.usecases import (
    CrearPaciente,
    ObtenerPaciente,
    ListarPacientes,
    ActualizarPaciente,
    EliminarPaciente
)
from app.domain.entities import Paciente as PacienteEntity
from app.domain.ports import PacienteRepository
from app.db.session import get_db
from app.adapters.database.models import PacienteRepositoryImpl


router = APIRouter(prefix="/api/pacientes", tags=["pacientes"])


def get_paciente_repo(db=Depends(get_db)) -> PacienteRepository:
    """Inyectar el repositorio de Paciente"""
    return PacienteRepositoryImpl(db)
    from app.adapters.database import PacienteRepositoryImpl
    return PacienteRepositoryImpl(db)


@router.post("/", response_model=PacienteResponse)
async def crear_paciente(
    datos: PacienteCreate,
    repo: PacienteRepository = Depends(get_paciente_repo)
) -> PacienteResponse:
    """Crear un nuevo paciente"""
    use_case = CrearPaciente(repo)
    try:
        paciente = await use_case.ejecutar(datos.dict())
        return PacienteResponse.from_orm(paciente)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{paciente_id}", response_model=PacienteResponse)
async def obtener_paciente(
    paciente_id: int,
    repo: PacienteRepository = Depends(get_paciente_repo)
) -> PacienteResponse:
    """Obtener un paciente por ID"""
    use_case = ObtenerPaciente(repo)
    try:
        paciente = await use_case.ejecutar(paciente_id)
        if not paciente:
            raise HTTPException(status_code=404, detail="Paciente no encontrado")
        return PacienteResponse.from_orm(paciente)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[PacienteResponse])
async def listar_pacientes(
    skip: int = 0,
    limit: int = 10,
    repo: PacienteRepository = Depends(get_paciente_repo)
) -> List[PacienteResponse]:
    """Listar pacientes con paginación"""
    use_case = ListarPacientes(repo)
    try:
        pacientes = await use_case.ejecutar(skip, limit)
        return [PacienteResponse.from_orm(p) for p in pacientes]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{paciente_id}", response_model=PacienteResponse)
async def actualizar_paciente(
    paciente_id: int,
    datos: PacienteCreate,
    repo: PacienteRepository = Depends(get_paciente_repo)
) -> PacienteResponse:
    """Actualizar un paciente"""
    use_case = ActualizarPaciente(repo)
    try:
        paciente = await use_case.ejecutar(paciente_id, datos.dict(exclude_unset=True))
        if not paciente:
            raise HTTPException(status_code=404, detail="Paciente no encontrado")
        return PacienteResponse.from_orm(paciente)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{paciente_id}")
async def eliminar_paciente(
    paciente_id: int,
    repo: PacienteRepository = Depends(get_paciente_repo)
) -> dict:
    """Eliminar un paciente"""
    use_case = EliminarPaciente(repo)
    try:
        exito = await use_case.ejecutar(paciente_id)
        if not exito:
            raise HTTPException(status_code=404, detail="Paciente no encontrado")
        return {"mensaje": "Paciente eliminado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
