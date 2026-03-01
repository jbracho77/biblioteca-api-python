from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime 

class LibroBase(BaseModel):
    id: int
    titulo: str = Field(..., min_length=1, max_length=100)
    autor: str = Field(..., min_length=3, max_length=50)
    categoria: str = Field("General", min_length=3, max_length=20) # Nuevo campo
    disponible: bool = True
    activo: bool = True
    fecha_prestamo: Optional[datetime] = None 
    usuario_prestamo: Optional[str] = None

    class Config:
        from_attributes = True

# Esto nos servirá por si luego queremos crear esquemas distintos para crear o actualizar
class Libro(LibroBase):
    pass
