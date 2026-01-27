from pydantic import BaseModel
from datetime import datetime

class CitaRequest(BaseModel):
    cliente: str
    fechas_iniciales: list[datetime]