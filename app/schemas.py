from pydantic import BaseModel, Field
from typing import Optional

class LibroBase(BaseModel):
    id: int
    titulo: str = Field(..., min_length=1, max_length=100)
    autor: str = Field(..., min_length=3, max_length=50)
    disponible: bool = True
    activo: bool = True

    class Config:
        from_attributes = True

# Esto nos servirá por si luego queremos crear esquemas distintos para crear o actualizar
class Libro(LibroBase):
    pass