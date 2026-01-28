from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
import sys

# Rutas (Adaptadores API - Hexagonal)
from app.adapters.api.routes.pacientes import router as pacientes_router
from app.adapters.api.routes.citas import router as citas_router

# Base de Datos (Session y Configuración)
from app.db.base import Base
from app.db.session import engine, get_db, SessionLocal

# Importar modelos ORM para registrar las tablas
from app.adapters.database.models import (
    PacienteORM, FisioterapeutaORM, MaquinaORM, EspacioORM,
    BloqueHorarioORM, ReservaORM, DiagnosticoORM, CitaORM
)

# Contenedor de DI
from app.shared.container import init_container


# ==================== STARTUP/SHUTDOWN ====================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gestionar el ciclo de vida de la aplicación
    """
    # Startup
    print("🚀 Iniciando aplicación...")
    
    try:
        # Crear tablas en la base de datos
        Base.metadata.create_all(bind=engine)
        print("✅ Base de datos PostgreSQL inicializada")
        
        # Inicializar contenedor de DI
        db = SessionLocal()
        init_container(db)
        print("✅ Contenedor de inyección de dependencias inicializado")
    except Exception as e:
        print(f"❌ Error al iniciar la aplicación: {e}")
        sys.exit(1)
    
    yield
    
    # Shutdown
    print("🛑 Cerrando aplicación...")
    db.close()
    print("✅ Aplicación cerrada")


# ==================== CONFIGURACIÓN DE FASTAPI ====================

app = FastAPI(
    title="API de Fisioterapia",
    description="Sistema de gestión de citas y reservas con arquitectura hexagonal",
    version="2.0.0",
    lifespan=lifespan
)


# ==================== RUTAS (ADAPTADORES HEXAGONALES) ====================

# Rutas de Pacientes
app.include_router(pacientes_router)

# Rutas de Citas
app.include_router(citas_router)


# ==================== HEALTH CHECK ====================

@app.get("/")
def health_check():
    return {
        "status": "ok",
        "message": "Sistema de Fisioterapia v2.0",
        "architecture": "hexagonal"
    }


@app.get("/health")
def detailed_health():
    return {
        "status": "healthy",
        "version": "2.0.0",
        "components": {
            "database": "initialized",
            "di_container": "initialized",
            "api": "running"
        }
    }
