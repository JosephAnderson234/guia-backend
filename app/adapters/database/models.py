"""
Adaptador de Base de Datos - PostgreSQL con SQLAlchemy
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean, Date, Time, Index
from sqlalchemy.orm import relationship, Session
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


# ==================== MODELOS ORM POSTGRESQL ====================

class FisioterapeutaORM(Base):
    """Modelo ORM de Fisioterapeuta"""
    __tablename__ = "fisioterapeutas"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False, unique=True)

    reservas = relationship("ReservaORM", back_populates="fisioterapeuta", cascade="all, delete-orphan")


class MaquinaORM(Base):
    """Modelo ORM de Máquina"""
    __tablename__ = "maquinas"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    codigo = Column(String(50), nullable=False, unique=True, index=True)

    reservas = relationship("ReservaORM", back_populates="maquina", cascade="all, delete-orphan")


class EspacioORM(Base):
    """Modelo ORM de Espacio"""
    __tablename__ = "espacios"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False, unique=True)

    reservas = relationship("ReservaORM", back_populates="espacio", cascade="all, delete-orphan")


class BloqueHorarioORM(Base):
    """Modelo ORM de Bloque Horario"""
    __tablename__ = "bloques_horarios"

    id = Column(Integer, primary_key=True)
    hora_inicio = Column(Time, nullable=False)
    hora_fin = Column(Time, nullable=False)

    reservas = relationship("ReservaORM", back_populates="bloque_horario", cascade="all, delete-orphan")
    
    __table_args__ = (
        Index('ix_bloques_horarios_inicio_fin', 'hora_inicio', 'hora_fin'),
        {'extend_existing': True}
    )


class PacienteORM(Base):
    """Modelo ORM de Paciente"""
    __tablename__ = "pacientes"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False, index=True)
    telefono = Column(Integer)
    fecha_nacimiento = Column(Date)
    centro_terapia_id = Column(Integer)
    usa_magneto = Column(Boolean, default=False)
    requiere_tratamiento_especial = Column(Boolean, default=False)
    seguro_medico = Column(Boolean, default=False)
    aseguradora = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    reservas = relationship("ReservaORM", back_populates="paciente", cascade="all, delete-orphan")
    diagnosticos = relationship("DiagnosticoORM", back_populates="paciente", cascade="all, delete-orphan")
    
    __table_args__ = (
        Index('ix_pacientes_nombre_created', 'nombre', 'created_at'),
        {'extend_existing': True}
    )


class ReservaORM(Base):
    """Modelo ORM de Reserva"""
    __tablename__ = "reservas"

    id = Column(Integer, primary_key=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id", ondelete="CASCADE"), nullable=False)
    fisioterapeuta_id = Column(Integer, ForeignKey("fisioterapeutas.id", ondelete="CASCADE"), nullable=False)
    espacio_id = Column(Integer, ForeignKey("espacios.id", ondelete="CASCADE"), nullable=False)
    bloque_id = Column(Integer, ForeignKey("bloques_horarios.id", ondelete="CASCADE"), nullable=False)
    maquina_id = Column(Integer, ForeignKey("maquinas.id", ondelete="SET NULL"), nullable=True)
    fecha = Column(Date, nullable=False, index=True)

    paciente = relationship("PacienteORM", back_populates="reservas")
    fisioterapeuta = relationship("FisioterapeutaORM", back_populates="reservas")
    espacio = relationship("EspacioORM", back_populates="reservas")
    bloque_horario = relationship("BloqueHorarioORM", back_populates="reservas")
    maquina = relationship("MaquinaORM", back_populates="reservas")
    
    __table_args__ = (
        Index('ix_reservas_paciente_fecha', 'paciente_id', 'fecha'),
        Index('ix_reservas_fisio_fecha', 'fisioterapeuta_id', 'fecha'),
        {'extend_existing': True}
    )


class DiagnosticoORM(Base):
    """Modelo ORM de Diagnóstico"""
    __tablename__ = "diagnosticos"

    id = Column(Integer, primary_key=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id", ondelete="CASCADE"), nullable=False)
    sessions = Column(Integer, nullable=False)
    treatment = Column(String(255), nullable=False)

    paciente = relationship("PacienteORM", back_populates="diagnosticos")
    
    __table_args__ = (
        Index('ix_diagnosticos_paciente', 'paciente_id'),
        {'extend_existing': True}
    )


class CitaORM(Base):
    """Modelo ORM de Cita"""
    __tablename__ = "citas"

    id = Column(Integer, primary_key=True)
    titulo = Column(String(200), nullable=False)
    descripcion = Column(Text)
    inicio = Column(DateTime, nullable=False, index=True)
    fin = Column(DateTime, nullable=False)
    email = Column(String(100), index=True)
    google_event_id = Column(String(255), unique=True, nullable=False, index=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        Index('ix_citas_inicio_fin', 'inicio', 'fin'),
        {'extend_existing': True}
    )


# ==================== IMPLEMENTACIONES DE REPOSITORIES ====================

class PacienteRepositoryImpl(PacienteRepository):
    """Implementación de PacienteRepository con PostgreSQL"""
    
    def __init__(self, db: Session):
        self.db = db
    
    async def crear(self, paciente: PacienteEntity) -> PacienteEntity:
        db_paciente = PacienteORM(**{k: v for k, v in paciente.__dict__.items() if v is not None})
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
    
    async def actualizar(self, paciente_id: int, datos: dict) -> Optional[PacienteEntity]:
        db_paciente = self.db.query(PacienteORM).filter(PacienteORM.id == paciente_id).first()
        if not db_paciente:
            return None
        for key, value in datos.items():
            if hasattr(db_paciente, key) and value is not None:
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
    def _to_entity(orm: PacienteORM) -> Optional[PacienteEntity]:
        if not orm:
            return None
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


class FisioterapeutaRepositoryImpl(FisioterapeutaRepository):
    """Implementación de FisioterapeutaRepository con PostgreSQL"""
    
    def __init__(self, db: Session):
        self.db = db
    
    async def crear(self, fisioterapeuta: FisioterapeutaEntity) -> FisioterapeutaEntity:
        db_fisio = FisioterapeutaORM(nombre=fisioterapeuta.nombre)
        self.db.add(db_fisio)
        self.db.commit()
        self.db.refresh(db_fisio)
        return self._to_entity(db_fisio)
    
    async def obtener_por_id(self, fisioterapeuta_id: int) -> Optional[FisioterapeutaEntity]:
        db_fisio = self.db.query(FisioterapeutaORM).filter(FisioterapeutaORM.id == fisioterapeuta_id).first()
        return self._to_entity(db_fisio) if db_fisio else None
    
    async def listar(self, skip: int = 0, limit: int = 100) -> List[FisioterapeutaEntity]:
        db_fisios = self.db.query(FisioterapeutaORM).offset(skip).limit(limit).all()
        return [self._to_entity(f) for f in db_fisios]
    
    async def contar_pacientes_en_bloque(self, fisioterapeuta_id: int, fecha: Date, bloque_id: int) -> int:
        """Cuenta cuántos pacientes tiene el fisio en un bloque específico"""
        count = self.db.query(ReservaORM).filter(
            ReservaORM.fisioterapeuta_id == fisioterapeuta_id,
            ReservaORM.fecha == fecha,
            ReservaORM.bloque_id == bloque_id
        ).count()
        return count
    
    async def tiene_paciente_con_trato_especial(self, fisioterapeuta_id: int, fecha: Date, bloque_id: int) -> bool:
        """Verifica si el fisio tiene un paciente con trato especial en ese bloque"""
        reserva = self.db.query(ReservaORM).join(
            PacienteORM, ReservaORM.paciente_id == PacienteORM.id
        ).filter(
            ReservaORM.fisioterapeuta_id == fisioterapeuta_id,
            ReservaORM.fecha == fecha,
            ReservaORM.bloque_id == bloque_id,
            PacienteORM.requiere_tratamiento_especial == True
        ).first()
        return reserva is not None
    
    @staticmethod
    def _to_entity(orm: FisioterapeutaORM) -> Optional[FisioterapeutaEntity]:
        if not orm:
            return None
        return FisioterapeutaEntity(id=orm.id, nombre=orm.nombre)


class EspacioRepositoryImpl(EspacioRepository):
    """Implementación de EspacioRepository con PostgreSQL"""
    
    def __init__(self, db: Session):
        self.db = db
    
    async def crear(self, espacio: EspacioEntity) -> EspacioEntity:
        db_espacio = EspacioORM(nombre=espacio.nombre)
        self.db.add(db_espacio)
        self.db.commit()
        self.db.refresh(db_espacio)
        return self._to_entity(db_espacio)
    
    async def obtener_por_id(self, espacio_id: int) -> Optional[EspacioEntity]:
        db_espacio = self.db.query(EspacioORM).filter(EspacioORM.id == espacio_id).first()
        return self._to_entity(db_espacio) if db_espacio else None
    
    async def listar(self, skip: int = 0, limit: int = 100) -> List[EspacioEntity]:
        db_espacios = self.db.query(EspacioORM).offset(skip).limit(limit).all()
        return [self._to_entity(e) for e in db_espacios]
    
    async def obtener_espacios_ocupados(self, fecha: Date, bloque_id: int) -> List[int]:
        """Obtiene IDs de espacios ocupados en una fecha y bloque específicos"""
        reservas = self.db.query(ReservaORM.espacio_id).filter(
            ReservaORM.fecha == fecha,
            ReservaORM.bloque_id == bloque_id
        ).all()
        return [r.espacio_id for r in reservas]
    
    async def esta_disponible(self, espacio_id: int, fecha: Date, bloque_id: int) -> bool:
        """Verifica si un espacio está disponible"""
        reserva = self.db.query(ReservaORM).filter(
            ReservaORM.espacio_id == espacio_id,
            ReservaORM.fecha == fecha,
            ReservaORM.bloque_id == bloque_id
        ).first()
        return reserva is None
    
    @staticmethod
    def _to_entity(orm: EspacioORM) -> Optional[EspacioEntity]:
        if not orm:
            return None
        return EspacioEntity(id=orm.id, nombre=orm.nombre)


class BloqueHorarioRepositoryImpl(BloqueHorarioRepository):
    """Implementación de BloqueHorarioRepository con PostgreSQL"""
    
    def __init__(self, db: Session):
        self.db = db
    
    async def crear(self, bloque: BloqueHorarioEntity) -> BloqueHorarioEntity:
        db_bloque = BloqueHorarioORM(hora_inicio=bloque.hora_inicio, hora_fin=bloque.hora_fin)
        self.db.add(db_bloque)
        self.db.commit()
        self.db.refresh(db_bloque)
        return self._to_entity(db_bloque)
    
    async def obtener_por_id(self, bloque_id: int) -> Optional[BloqueHorarioEntity]:
        db_bloque = self.db.query(BloqueHorarioORM).filter(BloqueHorarioORM.id == bloque_id).first()
        return self._to_entity(db_bloque) if db_bloque else None
    
    async def listar(self, skip: int = 0, limit: int = 100) -> List[BloqueHorarioEntity]:
        db_bloques = self.db.query(BloqueHorarioORM).order_by(BloqueHorarioORM.hora_inicio).offset(skip).limit(limit).all()
        return [self._to_entity(b) for b in db_bloques]
    
    @staticmethod
    def _to_entity(orm: BloqueHorarioORM) -> Optional[BloqueHorarioEntity]:
        if not orm:
            return None
        return BloqueHorarioEntity(
            id=orm.id,
            hora_inicio=orm.hora_inicio,
            hora_fin=orm.hora_fin
        )


class MaquinaRepositoryImpl(MaquinaRepository):
    """Implementación de MaquinaRepository con PostgreSQL"""
    
    def __init__(self, db: Session):
        self.db = db
    
    async def crear(self, maquina: MaquinaEntity) -> MaquinaEntity:
        db_maquina = MaquinaORM(codigo=maquina.codigo)
        self.db.add(db_maquina)
        self.db.commit()
        self.db.refresh(db_maquina)
        return self._to_entity(db_maquina)
    
    async def obtener_por_id(self, maquina_id: int) -> Optional[MaquinaEntity]:
        db_maquina = self.db.query(MaquinaORM).filter(MaquinaORM.id == maquina_id).first()
        return self._to_entity(db_maquina) if db_maquina else None
    
    async def listar(self, skip: int = 0, limit: int = 100) -> List[MaquinaEntity]:
        db_maquinas = self.db.query(MaquinaORM).offset(skip).limit(limit).all()
        return [self._to_entity(m) for m in db_maquinas]
    
    async def contar_maquinas_en_uso(self, fecha: Date, bloque_id: int) -> int:
        """Cuenta cuántas máquinas están en uso en un bloque específico"""
        count = self.db.query(ReservaORM).filter(
            ReservaORM.fecha == fecha,
            ReservaORM.bloque_id == bloque_id,
            ReservaORM.maquina_id.isnot(None)
        ).count()
        return count
    
    async def obtener_maquina_disponible(self, fecha: Date, bloque_id: int) -> Optional[int]:
        """Obtiene el ID de una máquina disponible, si existe"""
        maquinas_en_uso = self.db.query(ReservaORM.maquina_id).filter(
            ReservaORM.fecha == fecha,
            ReservaORM.bloque_id == bloque_id,
            ReservaORM.maquina_id.isnot(None)
        ).all()
        
        ids_en_uso = {m.maquina_id for m in maquinas_en_uso}
        
        maquina_libre = self.db.query(MaquinaORM).filter(
            ~MaquinaORM.id.in_(ids_en_uso)
        ).first()
        
        return maquina_libre.id if maquina_libre else None
    
    @staticmethod
    def _to_entity(orm: MaquinaORM) -> Optional[MaquinaEntity]:
        if not orm:
            return None
        return MaquinaEntity(id=orm.id, codigo=orm.codigo)


class ReservaRepositoryImpl(ReservaRepository):
    """Implementación de ReservaRepository con PostgreSQL"""
    
    def __init__(self, db: Session):
        self.db = db
    
    async def crear(self, reserva: ReservaEntity) -> ReservaEntity:
        db_reserva = ReservaORM(
            paciente_id=reserva.paciente_id,
            fisioterapeuta_id=reserva.fisioterapeuta_id,
            espacio_id=reserva.espacio_id,
            bloque_id=reserva.bloque_id,
            maquina_id=reserva.maquina_id,
            fecha=reserva.fecha
        )
        self.db.add(db_reserva)
        self.db.commit()
        self.db.refresh(db_reserva)
        return self._to_entity(db_reserva)
    
    async def obtener_por_id(self, reserva_id: int) -> Optional[ReservaEntity]:
        db_reserva = self.db.query(ReservaORM).filter(ReservaORM.id == reserva_id).first()
        return self._to_entity(db_reserva) if db_reserva else None
    
    async def listar(self, skip: int = 0, limit: int = 100) -> List[ReservaEntity]:
        db_reservas = self.db.query(ReservaORM).offset(skip).limit(limit).all()
        return [self._to_entity(r) for r in db_reservas]
    
    async def listar_por_paciente(self, paciente_id: int) -> List[ReservaEntity]:
        """Lista todas las reservas de un paciente"""
        db_reservas = self.db.query(ReservaORM).filter(
            ReservaORM.paciente_id == paciente_id
        ).order_by(ReservaORM.fecha).all()
        return [self._to_entity(r) for r in db_reservas]
    
    async def listar_por_fecha_bloque(self, fecha: Date, bloque_id: int) -> List[ReservaEntity]:
        """Lista reservas de una fecha y bloque específicos"""
        db_reservas = self.db.query(ReservaORM).filter(
            ReservaORM.fecha == fecha,
            ReservaORM.bloque_id == bloque_id
        ).all()
        return [self._to_entity(r) for r in db_reservas]
    
    @staticmethod
    def _to_entity(orm: ReservaORM) -> Optional[ReservaEntity]:
        if not orm:
            return None
        return ReservaEntity(
            id=orm.id,
            paciente_id=orm.paciente_id,
            fisioterapeuta_id=orm.fisioterapeuta_id,
            espacio_id=orm.espacio_id,
            bloque_id=orm.bloque_id,
            maquina_id=orm.maquina_id,
            fecha=orm.fecha
        )
      
