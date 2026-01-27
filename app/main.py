from fastapi import FastAPI
from app.routes.citas import router as citas_router
# from app.db.base import Base
# from app.db.session import engine
# COMENTADO: Persistencia a BD deshabilitada
# Con Alembic puedes controlar cambios en el esquema de forma segura
# alembic init migrations
# alembic revision --autogenerate -m "descripción"
# alembic upgrade head

app = FastAPI(
    title="API de Citas",
    description="Sistema de agendamiento con Google Calendar",
    version="1.0.0"
)

# Registrar rutas
app.include_router(citas_router)

@app.get("/")
def health_check():
    return {"status": "ok"}
