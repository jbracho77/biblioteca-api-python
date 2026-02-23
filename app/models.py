from sqlalchemy import Column, Integer, String, Boolean
from .database import Base

class LibroDB(Base):
    __tablename__ = "libros"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String)
    autor = Column(String)
    disponible = Column(Boolean, default=True)
    activo = Column(Boolean, default=True)