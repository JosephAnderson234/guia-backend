#!/usr/bin/env python
"""
Script para inicializar la base de datos PostgreSQL
Uso: 
    python init_db.py         # Crear tablas
    python init_db.py drop    # Eliminar todas las tablas
    python init_db.py reset   # Eliminar y recrear tablas
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
    print("\n" + "="*70)
    print("🔄 Creando tablas en PostgreSQL...")
    print("="*70 + "\n")
    
    Base.metadata.create_all(bind=engine)
    
    # Mostrar tablas creadas
    from sqlalchemy import inspect
    inspector = inspect(engine)
    tablas = inspector.get_table_names()
    
    print("✅ Tablas creadas exitosamente:\n")
    for tabla in tablas:
        print(f"   • {tabla}")
    
    print("\n" + "="*70)
    print("✅ Base de datos inicializada correctamente")
    print("="*70)
    print("\n💡 Para insertar datos de prueba, ejecuta:")
    print("   psql -U postgres -d fisioterapia_db -f datos_prueba_citas.sql\n")


def drop_db():
    """Eliminar todas las tablas de la base de datos"""
    print("\n" + "="*70)
    print("⚠️  ADVERTENCIA: Eliminando TODAS las tablas...")
    print("="*70 + "\n")
    
    respuesta = input("¿Estás seguro? Esta acción NO se puede deshacer (s/N): ")
    
    if respuesta.lower() in ['s', 'si', 'sí', 'y', 'yes']:
        Base.metadata.drop_all(bind=engine)
        print("\n✅ Tablas eliminadas exitosamente\n")
    else:
        print("\n❌ Operación cancelada\n")


def reset_db():
    """Eliminar y recrear todas las tablas"""
    print("\n" + "="*70)
    print("⚠️  RESET: Eliminando y recreando TODAS las tablas...")
    print("="*70 + "\n")
    
    respuesta = input("¿Estás seguro? Perderás TODOS los datos (s/N): ")
    
    if respuesta.lower() in ['s', 'si', 'sí', 'y', 'yes']:
        print("\n🗑️  Eliminando tablas...")
        Base.metadata.drop_all(bind=engine)
        print("✅ Tablas eliminadas\n")
        
        print("🔄 Recreando tablas...")
        Base.metadata.create_all(bind=engine)
        
        # Mostrar tablas creadas
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tablas = inspector.get_table_names()
        
        print("✅ Tablas recreadas:\n")
        for tabla in tablas:
            print(f"   • {tabla}")
        
        print("\n" + "="*70)
        print("✅ Base de datos reseteada correctamente")
        print("="*70)
        print("\n💡 Para insertar datos de prueba, ejecuta:")
        print("   psql -U postgres -d fisioterapia_db -f datos_prueba_citas.sql\n")
    else:
        print("\n❌ Operación cancelada\n")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        comando = sys.argv[1].lower()
        if comando == "drop":
            drop_db()
        elif comando == "reset":
            reset_db()
        else:
            print(f"\n❌ Comando '{comando}' no reconocido")
            print("\nUso:")
            print("  python init_db.py         # Crear tablas")
            print("  python init_db.py drop    # Eliminar todas las tablas")
            print("  python init_db.py reset   # Eliminar y recrear tablas\n")
    else:
        init_db()
