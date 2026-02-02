"""
Casos de Uso - Lógica de aplicación
"""

from typing import List, Optional, Dict, Any
from datetime import date, timedelta
from app.domain.entities import Paciente, Reserva, Diagnostico
from app.domain.ports import (
    PacienteRepository,
    ReservaRepository,
    DiagnosticoRepository,
    FisioterapeutaRepository,
    EspacioRepository,
    BloqueHorarioRepository,
    MaquinaRepository
)
from sqlalchemy.orm import Session


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


class ConsultarDisponibilidad:
    """Caso de uso: Consultar disponibilidad de bloques horarios"""
    
    def __init__(
        self,
        espacio_repo: EspacioRepository,
        bloque_repo: BloqueHorarioRepository,
        fisio_repo: FisioterapeutaRepository,
        maquina_repo: MaquinaRepository,
        paciente_repo: PacienteRepository
    ):
        self.espacio_repo = espacio_repo
        self.bloque_repo = bloque_repo
        self.fisio_repo = fisio_repo
        self.maquina_repo = maquina_repo
        self.paciente_repo = paciente_repo
    
    async def ejecutar(
        self,
        fecha_inicio: date,
        fecha_fin: date,
        paciente_id: Optional[int] = None,
        fisioterapeuta_id: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Retorna bloques disponibles para un rango de fechas.
        
        Args:
            fecha_inicio: Fecha inicial del rango
            fecha_fin: Fecha final del rango
            paciente_id: ID del paciente (opcional, para validar si requiere máquina)
            fisioterapeuta_id: ID del fisioterapeuta (opcional, para filtrar disponibilidad)
        
        Returns:
            Lista de bloques disponibles con información de espacios, fisios y máquinas
        """
        # Obtener todos los bloques horarios
        bloques = await self.bloque_repo.listar(limit=100)
        
        # Obtener todos los espacios (máximo 9)
        espacios = await self.espacio_repo.listar(limit=9)
        
        # Verificar si el paciente requiere máquina
        requiere_maquina = False
        if paciente_id:
            paciente = await self.paciente_repo.obtener_por_id(paciente_id)
            if paciente:
                requiere_maquina = paciente.usa_magneto
        
        disponibilidad = []
        
        # Iterar por cada fecha en el rango
        fecha_actual = fecha_inicio
        while fecha_actual <= fecha_fin:
            for bloque in bloques:
                # Contar espacios ocupados
                espacios_ocupados = await self.espacio_repo.obtener_espacios_ocupados(
                    fecha_actual, bloque.id
                )
                espacios_libres = len(espacios) - len(espacios_ocupados)
                
                # Si se especificó un fisioterapeuta, validar su disponibilidad
                fisio_disponible = True
                if fisioterapeuta_id:
                    # Contar pacientes actuales del fisio en este bloque
                    pacientes_fisio = await self.fisio_repo.contar_pacientes_en_bloque(
                        fisioterapeuta_id, fecha_actual, bloque.id
                    )
                    
                    # Verificar si tiene paciente con trato especial
                    tiene_trato_especial = await self.fisio_repo.tiene_paciente_con_trato_especial(
                        fisioterapeuta_id, fecha_actual, bloque.id
                    )
                    
                    # Si ya tiene trato especial, no puede atender más pacientes
                    if tiene_trato_especial:
                        fisio_disponible = False
                    # Si ya tiene 2 pacientes, no puede atender más
                    elif pacientes_fisio >= 2:
                        fisio_disponible = False
                
                # Validar disponibilidad de máquinas si se requiere
                maquinas_disponibles = 3  # Total de máquinas
                if requiere_maquina:
                    maquinas_en_uso = await self.maquina_repo.contar_maquinas_en_uso(
                        fecha_actual, bloque.id
                    )
                    maquinas_disponibles = 3 - maquinas_en_uso
                
                # Solo agregar si hay disponibilidad
                if (espacios_libres > 0 and fisio_disponible and 
                    (not requiere_maquina or maquinas_disponibles > 0)):
                    disponibilidad.append({
                        "fecha": fecha_actual,
                        "bloque_id": bloque.id,
                        "hora_inicio": bloque.hora_inicio,
                        "hora_fin": bloque.hora_fin,
                        "espacios_disponibles": espacios_libres,
                        "maquinas_disponibles": maquinas_disponibles if requiere_maquina else None
                    })
            
            fecha_actual += timedelta(days=1)
        
        return disponibilidad


class AgendarTratamientoRecurrente:
    """Caso de uso: Agendar tratamiento recurrente semanal"""
    
    def __init__(
        self,
        db: Session,
        paciente_repo: PacienteRepository,
        fisio_repo: FisioterapeutaRepository,
        espacio_repo: EspacioRepository,
        bloque_repo: BloqueHorarioRepository,
        maquina_repo: MaquinaRepository,
        reserva_repo: ReservaRepository
    ):
        self.db = db
        self.paciente_repo = paciente_repo
        self.fisio_repo = fisio_repo
        self.espacio_repo = espacio_repo
        self.bloque_repo = bloque_repo
        self.maquina_repo = maquina_repo
        self.reserva_repo = reserva_repo
    
    async def ejecutar(
        self,
        paciente_id: int,
        fisioterapeuta_id: int,
        bloque_id: int,
        fecha_inicio: date,
        total_sesiones: int,
        requiere_maquina: bool = False
    ) -> List[Reserva]:
        """
        Agenda un tratamiento recurrente semanal.
        
        Reglas:
        - Máximo 3 sesiones por semana
        - Mismo día de la semana y mismo bloque horario
        - Validación completa de todas las reglas de negocio
        - Uso de transacciones para atomicidad
        
        Args:
            paciente_id: ID del paciente
            fisioterapeuta_id: ID del fisioterapeuta
            bloque_id: ID del bloque horario
            fecha_inicio: Fecha de inicio del tratamiento
            total_sesiones: Número total de sesiones a agendar
            requiere_maquina: Si el paciente requiere máquina
        
        Returns:
            Lista de reservas creadas
        
        Raises:
            ValueError: Si alguna validación falla
        """
        # Validar que paciente y fisioterapeuta existen
        paciente = await self.paciente_repo.obtener_por_id(paciente_id)
        if not paciente:
            raise ValueError(f"Paciente {paciente_id} no encontrado")
        
        fisioterapeuta = await self.fisio_repo.obtener_por_id(fisioterapeuta_id)
        if not fisioterapeuta:
            raise ValueError(f"Fisioterapeuta {fisioterapeuta_id} no encontrado")
        
        bloque = await self.bloque_repo.obtener_por_id(bloque_id)
        if not bloque:
            raise ValueError(f"Bloque horario {bloque_id} no encontrado")
        
        # Calcular fechas semanales (máximo 3 sesiones por semana)
        fechas_sesiones = self._calcular_fechas_semanales(fecha_inicio, total_sesiones)
        
        # Iniciar transacción
        with self.db.begin():
            reservas_creadas = []
            
            # Validar y crear cada reserva
            for fecha_sesion in fechas_sesiones:
                # Validar disponibilidad de espacio
                espacios_ocupados = await self.espacio_repo.obtener_espacios_ocupados(
                    fecha_sesion, bloque_id
                )
                
                # Obtener todos los espacios y encontrar uno libre
                espacios = await self.espacio_repo.listar(limit=9)
                espacio_id = None
                for espacio in espacios:
                    if espacio.id not in espacios_ocupados:
                        espacio_id = espacio.id
                        break
                
                if not espacio_id:
                    raise ValueError(
                        f"No hay espacios disponibles para {fecha_sesion} en bloque {bloque_id}"
                    )
                
                # Validar capacidad del fisioterapeuta
                pacientes_fisio = await self.fisio_repo.contar_pacientes_en_bloque(
                    fisioterapeuta_id, fecha_sesion, bloque_id
                )
                
                tiene_trato_especial = await self.fisio_repo.tiene_paciente_con_trato_especial(
                    fisioterapeuta_id, fecha_sesion, bloque_id
                )
                
                # Si el paciente requiere trato especial, el fisio no puede tener otros pacientes
                if paciente.requiere_tratamiento_especial and pacientes_fisio > 0:
                    raise ValueError(
                        f"Fisioterapeuta {fisioterapeuta_id} ya tiene pacientes en {fecha_sesion} "
                        f"bloque {bloque_id} y el paciente requiere trato especial"
                    )
                
                # Si el fisio ya tiene un paciente con trato especial, no puede atender más
                if tiene_trato_especial:
                    raise ValueError(
                        f"Fisioterapeuta {fisioterapeuta_id} tiene un paciente con trato especial "
                        f"en {fecha_sesion} bloque {bloque_id}"
                    )
                
                # Si ya tiene 2 pacientes, no puede atender más
                if pacientes_fisio >= 2:
                    raise ValueError(
                        f"Fisioterapeuta {fisioterapeuta_id} ya tiene 2 pacientes en {fecha_sesion} "
                        f"bloque {bloque_id}"
                    )
                
                # Validar disponibilidad de máquinas si se requiere
                maquina_id = None
                if requiere_maquina:
                    maquinas_en_uso = await self.maquina_repo.contar_maquinas_en_uso(
                        fecha_sesion, bloque_id
                    )
                    
                    if maquinas_en_uso >= 3:
                        raise ValueError(
                            f"No hay máquinas disponibles para {fecha_sesion} en bloque {bloque_id}"
                        )
                    
                    maquina_id = await self.maquina_repo.obtener_maquina_disponible(
                        fecha_sesion, bloque_id
                    )
                    
                    if not maquina_id:
                        raise ValueError(
                            f"Error al asignar máquina para {fecha_sesion} en bloque {bloque_id}"
                        )
                
                # Crear la reserva
                reserva = Reserva(
                    paciente_id=paciente_id,
                    fisioterapeuta_id=fisioterapeuta_id,
                    espacio_id=espacio_id,
                    bloque_id=bloque_id,
                    maquina_id=maquina_id,
                    fecha=fecha_sesion
                )
                
                reserva_creada = await self.reserva_repo.crear(reserva)
                reservas_creadas.append(reserva_creada)
            
            return reservas_creadas
    
    def _calcular_fechas_semanales(self, fecha_inicio: date, total_sesiones: int) -> List[date]:
        """
        Calcula las fechas para sesiones semanales recurrentes.
        
        Reglas:
        - Máximo 3 sesiones por semana
        - Siempre el mismo día de la semana
        - Continúa en semanas siguientes hasta completar total_sesiones
        
        Args:
            fecha_inicio: Fecha de la primera sesión
            total_sesiones: Número total de sesiones a agendar
        
        Returns:
            Lista de fechas para las sesiones
        """
        fechas = []
        fecha_actual = fecha_inicio
        sesiones_restantes = total_sesiones
        
        while sesiones_restantes > 0:
            # Agregar máximo 3 sesiones por semana
            sesiones_esta_semana = min(3, sesiones_restantes)
            
            # Agregar la fecha actual
            fechas.append(fecha_actual)
            sesiones_restantes -= 1
            
            # Si quedan más sesiones en esta semana, agregar en días consecutivos
            for _ in range(sesiones_esta_semana - 1):
                if sesiones_restantes > 0:
                    fecha_actual += timedelta(days=1)
                    fechas.append(fecha_actual)
                    sesiones_restantes -= 1
            
            # Si quedan sesiones, pasar a la próxima semana (mismo día de la semana que fecha_inicio)
            if sesiones_restantes > 0:
                # Calcular días hasta el mismo día de la semana siguiente
                dias_hasta_misma_semana = 7 - (fecha_actual.weekday() - fecha_inicio.weekday()) % 7
                if dias_hasta_misma_semana == 0:
                    dias_hasta_misma_semana = 7
                fecha_actual += timedelta(days=dias_hasta_misma_semana)
        
        return fechas

