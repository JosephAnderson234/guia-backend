#!/usr/bin/env python
"""
Script para inicializar la base de datos PostgreSQL
Uso: python init_db.py
"""

from app.db.session import engine
from app.db.base import Base
from app.adapters.database.models import (
    PacienteORM,
    FisioterapeutaORM,
    MaquinaORM,
    EspacioORM,
    BloqueHorarioORM,
    ReservaORM,
    DiagnosticoORM,
    CitaORM
)


def init_db():
    """Crear todas las tablas en la base de datos"""
    print("🔄 Creando tablas en PostgreSQL...")
    Base.metadata.create_all(bind=engine)
    """Importar datos de prueba"""
    #usar datos_prueba_citas.sql para insertar datos de prueba
    
    
    
    print("✅ Base de datos inicializada exitosamente")


def drop_db():
    """Eliminar todas las tablas de la base de datos"""
    print("⚠️  Eliminando todas las tablas...")
    Base.metadata.drop_all(bind=engine)
    print("✅ Tablas eliminadas")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "drop":
        drop_db()
    else:
        init_db()
