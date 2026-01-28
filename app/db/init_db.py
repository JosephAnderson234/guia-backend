"""
Script para crear las tablas en la base de datos
Ejecutar una sola vez después de cambiar los modelos
"""

from app.db.session import engine
from app.db.base import Base
from app.db import models  # Importante: importar para registrar todos los modelos

def init_db():
    """Crea todas las tablas definidas en los modelos"""
    print("\n" + "="*60)
    print("🔄 Creando tablas en la base de datos...")
    print("="*60 + "\n")
    
    Base.metadata.create_all(bind=engine)
    
    # Mostrar tablas creadas
    from sqlalchemy import inspect
    inspector = inspect(engine)
    tablas = inspector.get_table_names()
    
    print("✅ Tablas creadas exitosamente:\n")
    for tabla in tablas:
        print(f"   • {tabla}")
    
    print("\n" + "="*60)
    print("✅ Base de datos inicializada correctamente")
    print("="*60 + "\n")

if __name__ == "__main__":
    init_db()
