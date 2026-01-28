"""
Rutas de la API - Adaptadores de FastAPI
"""

from .pacientes import router as pacientes_router

__all__ = ["pacientes_router"]
