"""
Rutas de la API - Adaptadores de FastAPI
"""

from .pacientes import router as pacientes_router
from .citas import router as citas_router

__all__ = ["pacientes_router", "citas_router"]
