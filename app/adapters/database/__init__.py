"""
Adaptador de Base de Datos - SQLAlchemy
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean, Date, Time
from sqlalchemy.orm import relationship, Session
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.db.base import Base
from app.domain.entities import (
    Paciente as PacienteEntity,
    Reserva as ReservaEntity,
    Diagnostico as DiagnosticoEntity,
    Fisioterapeuta as FisioterapeutaEntity,
    Maquina as MaquinaEntity,
    Espacio as EspacioEntity,
    BloqueHorario as BloqueHorarioEntity,
    Cita as CitaEntity
)
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
from datetime import datetime


# ==================== MODELOS SQLAlchemy ====================

class PacienteORM(Base):
    """Modelo ORM de Paciente"""
    __tablename__ = "pacientes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    telefono = Column(Integer)
    fecha_nacimiento = Column(Date)
    centro_terapia_id = Column(Integer)
    usa_magneto = Column(Boolean, default=False)
    requiere_tratamiento_especial = Column(Boolean, default=False)
    seguro_medico = Column(Boolean, default=False)
    aseguradora = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)

    reservas = relationship("ReservaORM", back_populates="paciente")
    diagnosticos = relationship("DiagnosticoORM", back_populates="paciente")


class FisioterapeutaORM(Base):
    """Modelo ORM de Fisioterapeuta"""
    __tablename__ = "fisioterapeutas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)

    reservas = relationship("ReservaORM", back_populates="fisioterapeuta")


class MaquinaORM(Base):
    """Modelo ORM de Máquina"""
    __tablename__ = "maquinas"

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String(50), unique=True, nullable=False)

    reservas = relationship("ReservaORM", back_populates="maquina")


class EspacioORM(Base):
    """Modelo ORM de Espacio"""
    __tablename__ = "espacios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)

    reservas = relationship("ReservaORM", back_populates="espacio")


class BloqueHorarioORM(Base):
    """Modelo ORM de Bloque Horario"""
    __tablename__ = "bloques_horarios"

    id = Column(Integer, primary_key=True, index=True)
    hora_inicio = Column(Time, nullable=False)
    hora_fin = Column(Time, nullable=False)

    reservas = relationship("ReservaORM", back_populates="bloque_horario")


class ReservaORM(Base):
    """Modelo ORM de Reserva"""
    __tablename__ = "reservas"

    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"), nullable=False)
    fisioterapeuta_id = Column(Integer, ForeignKey("fisioterapeutas.id"), nullable=False)
    espacio_id = Column(Integer, ForeignKey("espacios.id"), nullable=False, unique=True)
    bloque_id = Column(Integer, ForeignKey("bloques_horarios.id"), nullable=False, unique=True)
    maquina_id = Column(Integer, ForeignKey("maquinas.id"))
    fecha = Column(Date, nullable=False, unique=True)

    paciente = relationship("PacienteORM", back_populates="reservas")
    fisioterapeuta = relationship("FisioterapeutaORM", back_populates="reservas")
    espacio = relationship("EspacioORM", back_populates="reservas")
    bloque_horario = relationship("BloqueHorarioORM", back_populates="reservas")
    maquina = relationship("MaquinaORM", back_populates="reservas")


class DiagnosticoORM(Base):
    """Modelo ORM de Diagnóstico"""
    __tablename__ = "diagnosticos"

    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"), nullable=False)
    sessions = Column(Integer, nullable=False)
    treatment = Column(String(255), nullable=False)

    paciente = relationship("PacienteORM", back_populates="diagnosticos")


class CitaORM(Base):
    """Modelo ORM de Cita"""
    __tablename__ = "citas"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(200), nullable=False)
    descripcion = Column(Text)
    inicio = Column(DateTime, nullable=False)
    fin = Column(DateTime, nullable=False)
    email = Column(String(100))
    google_event_id = Column(String(255), unique=True, nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)


# ==================== IMPLEMENTACIONES DE REPOSITORIES ====================

class PacienteRepositoryImpl(PacienteRepository):
    """Implementación de PacienteRepository con SQLAlchemy"""
    
    def __init__(self, db: Session):
        self.db = db
    
    async def crear(self, paciente: PacienteEntity) -> PacienteEntity:
        db_paciente = PacienteORM(**paciente.__dict__)
        self.db.add(db_paciente)
        self.db.commit()
        self.db.refresh(db_paciente)
        return self._to_entity(db_paciente)
    
    async def obtener_por_id(self, paciente_id: int) -> Optional[PacienteEntity]:
        db_paciente = self.db.query(PacienteORM).filter(PacienteORM.id == paciente_id).first()
        return self._to_entity(db_paciente) if db_paciente else None
    
    async def listar(self, skip: int = 0, limit: int = 10) -> List[PacienteEntity]:
        db_pacientes = self.db.query(PacienteORM).offset(skip).limit(limit).all()
        return [self._to_entity(p) for p in db_pacientes]
    
    async def actualizar(self, paciente_id: int, datos: dict) -> PacienteEntity:
        db_paciente = self.db.query(PacienteORM).filter(PacienteORM.id == paciente_id).first()
        for key, value in datos.items():
            setattr(db_paciente, key, value)
        self.db.commit()
        self.db.refresh(db_paciente)
        return self._to_entity(db_paciente)
    
    async def eliminar(self, paciente_id: int) -> bool:
        db_paciente = self.db.query(PacienteORM).filter(PacienteORM.id == paciente_id).first()
        if db_paciente:
            self.db.delete(db_paciente)
            self.db.commit()
            return True
        return False
    
    @staticmethod
    def _to_entity(orm: PacienteORM) -> PacienteEntity:
        return PacienteEntity(
            id=orm.id,
            nombre=orm.nombre,
            telefono=orm.telefono,
            fecha_nacimiento=orm.fecha_nacimiento,
            centro_terapia_id=orm.centro_terapia_id,
            usa_magneto=orm.usa_magneto,
            requiere_tratamiento_especial=orm.requiere_tratamiento_especial,
            seguro_medico=orm.seguro_medico,
            aseguradora=orm.aseguradora,
            created_at=orm.created_at
        )
