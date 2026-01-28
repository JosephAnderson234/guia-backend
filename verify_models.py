#!/usr/bin/env python
"""Verificar que no hay tablas duplicadas"""
import sys
try:
    from app.db.session import engine
    from app.db.base import Base
    from app.adapters.database.models import (
        PacienteORM, FisioterapeutaORM, MaquinaORM, EspacioORM,
        BloqueHorarioORM, ReservaORM, DiagnosticoORM, CitaORM
    )
    
    print("✅ Importaciones correctas - No hay conflictos de tablas")
    print(f"✅ Total de tablas registradas: {len(Base.metadata.tables)}")
    print("\nTablas registradas:")
    for tabla in Base.metadata.tables.keys():
        print(f"  - {tabla}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)
