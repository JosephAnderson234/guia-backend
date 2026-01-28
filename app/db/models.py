from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean, Date, Time
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime, date, time

# ==================== FISIOTERAPIA: Modelos de Negocio ====================

class Fisioterapeuta(Base):
    """Modelo de Fisioterapeuta"""
    __tablename__ = "fisioterapeutas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)

    # Relaciones
    reservas = relationship("Reserva", back_populates="fisioterapeuta")


class Maquina(Base):
    """Modelo de Máquina de Terapia"""
    __tablename__ = "maquinas"

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String(50), unique=True, nullable=False)

    # Relaciones
    reservas = relationship("Reserva", back_populates="maquina")


class Espacio(Base):
    """Modelo de Espacio/Sala de Terapia"""
    __tablename__ = "espacios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)

    # Relaciones
    reservas = relationship("Reserva", back_populates="espacio")


class BloqueHorario(Base):
    """Modelo de Bloque Horario"""
    __tablename__ = "bloques_horarios"

    id = Column(Integer, primary_key=True, index=True)
    hora_inicio = Column(Time, nullable=False)
    hora_fin = Column(Time, nullable=False)

    # Relaciones
    reservas = relationship("Reserva", back_populates="bloque_horario")


class Paciente(Base):
    """Modelo de Paciente"""
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

    # Relaciones
    reservas = relationship("Reserva", back_populates="paciente")
    diagnosticos = relationship("Diagnostico", back_populates="paciente")


class Reserva(Base):
    """Modelo de Reserva de Cita de Terapia"""
    __tablename__ = "reservas"

    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"), nullable=False)
    fisioterapeuta_id = Column(Integer, ForeignKey("fisioterapeutas.id"), nullable=False)
    espacio_id = Column(Integer, ForeignKey("espacios.id"), nullable=False, unique=True)
    bloque_id = Column(Integer, ForeignKey("bloques_horarios.id"), nullable=False, unique=True)
    maquina_id = Column(Integer, ForeignKey("maquinas.id"))
    fecha = Column(Date, nullable=False, unique=True)

    # Relaciones
    paciente = relationship("Paciente", back_populates="reservas")
    fisioterapeuta = relationship("Fisioterapeuta", back_populates="reservas")
    espacio = relationship("Espacio", back_populates="reservas")
    bloque_horario = relationship("BloqueHorario", back_populates="reservas")
    maquina = relationship("Maquina", back_populates="reservas")


class Diagnostico(Base):
    """Modelo de Diagnóstico de Paciente"""
    __tablename__ = "diagnosticos"

    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"), nullable=False)
    sessions = Column(Integer, nullable=False)
    treatment = Column(String(255), nullable=False)

    # Relaciones
    paciente = relationship("Paciente", back_populates="diagnosticos")
