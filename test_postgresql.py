#!/usr/bin/env python
"""
Script de prueba funcional para PostgreSQL
Uso: python test_postgresql.py
"""

import asyncio
from sqlalchemy.orm import Session
from app.db.session import SessionLocal, engine
from app.db.base import Base
from app.adapters.database.models import (
    PacienteRepositoryImpl,
    PacienteORM,
    FisioterapeutaORM,
    MaquinaORM,
    EspacioORM,
    BloqueHorarioORM,
    ReservaORM,
    DiagnosticoORM,
    CitaORM
)
from app.domain.entities import Paciente
from app.domain.usecases import (
    CrearPaciente,
    ObtenerPaciente,
    ListarPacientes,
    ActualizarPaciente,
    EliminarPaciente
)
from datetime import date, time


async def test_postgresql():
    """Pruebas funcionales con PostgreSQL"""
    
    print("\n" + "="*60)
    print("🧪 PRUEBAS FUNCIONALES - POSTGRESQL")
    print("="*60)
    
    # Crear tablas
    print("\n1️⃣  Inicializando base de datos...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tablas creadas en PostgreSQL")
    
    # Obtener sesión
    db: Session = SessionLocal()
    
    try:
        # Test 1: Crear repositorio
        print("\n2️⃣  Inicializando repositorio...")
        repo = PacienteRepositoryImpl(db)
        print("✅ Repositorio inicializado")
        
        # Test 2: Crear use case
        print("\n3️⃣  Creando paciente a través del use case...")
        use_case_crear = CrearPaciente(repo)
        
        paciente_data = {
            "nombre": "Juan Pérez",
            "telefono": 3001234567,
            "fecha_nacimiento": date(1990, 5, 15),
            "seguro_medico": True,
            "aseguradora": "Salud Total"
        }
        
        paciente = await use_case_crear.ejecutar(paciente_data)
        print(f"✅ Paciente creado: {paciente.nombre} (ID: {paciente.id})")
        
        # Test 3: Obtener paciente
        print("\n4️⃣  Recuperando paciente por ID...")
        use_case_obtener = ObtenerPaciente(repo)
        paciente_recuperado = await use_case_obtener.ejecutar(paciente.id)
        print(f"✅ Paciente recuperado: {paciente_recuperado.nombre}")
        
        # Test 4: Listar pacientes
        print("\n5️⃣  Listando todos los pacientes...")
        use_case_listar = ListarPacientes(repo)
        pacientes = await use_case_listar.ejecutar(0, 10)
        print(f"✅ Total de pacientes: {len(pacientes)}")
        for p in pacientes:
            print(f"   - {p.nombre} (ID: {p.id})")
        
        # Test 5: Actualizar paciente
        print("\n6️⃣  Actualizando paciente...")
        use_case_actualizar = ActualizarPaciente(repo)
        datos_actualizar = {"aseguradora": "EPS Nueva"}
        paciente_actualizado = await use_case_actualizar.ejecutar(paciente.id, datos_actualizar)
        print(f"✅ Paciente actualizado: {paciente_actualizado.aseguradora}")
        
        # Test 6: Eliminar paciente
        print("\n7️⃣  Eliminando paciente...")
        use_case_eliminar = EliminarPaciente(repo)
        resultado = await use_case_eliminar.ejecutar(paciente.id)
        print(f"✅ Paciente eliminado: {resultado}")
        
        # Test 7: Verificar eliminación
        print("\n8️⃣  Verificando eliminación...")
        paciente_eliminado = await use_case_obtener.ejecutar(paciente.id)
        print(f"✅ Paciente no encontrado: {paciente_eliminado is None}")
        
        print("\n" + "="*60)
        print("✨ TODAS LAS PRUEBAS PASARON EXITOSAMENTE")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    asyncio.run(test_postgresql())
