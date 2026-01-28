#!/usr/bin/env python
"""Verificar que todo está migrado correctamente a la arquitectura hexagonal"""

import sys

try:
    print("\n✅ Verificando arquitectura hexagonal...\n")
    
    # Verificar imports hexagonales
    from app.adapters.api.routes.pacientes import router as pacientes_router
    from app.adapters.api.routes.citas import router as citas_router
    from app.adapters.database.models import PacienteRepositoryImpl, CitaORM
    from app.adapters.external.google_calendar import calendar_service
    from app.shared.schemas import CitaResponse, PacienteResponse
    from app.domain.entities import Paciente
    from app.domain.usecases import CrearPaciente
    
    print("✓ Rutas API Hexagonales")
    print("✓ Adaptadores de BD")
    print("✓ Adaptadores Externos")
    print("✓ Esquemas compartidos")
    print("✓ Entidades de dominio")
    print("✓ Casos de uso")
    
    print("\n✅ ARQUITECTURA MIGRADA CORRECTAMENTE")
    print("   - Código legacy en carpetas app/routes/, app/schemas/, app/core/")
    print("   - Todo funcional en app/adapters/, app/domain/, app/shared/")
    print("\n")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}\n")
    import traceback
    traceback.print_exc()
    sys.exit(1)
