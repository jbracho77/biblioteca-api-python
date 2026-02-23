from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy import Column, Integer, String, Boolean
from database import Base, engine

# Esto crea la tabla físicamente en el archivo .db si no existe
class LibroDB(Base):
    __tablename__ = "libros"
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String)
    autor = Column(String)
    disponible = Column(Boolean, default=True)
    activo = Column(Boolean, default=True)

from fastapi import Depends
from sqlalchemy.orm import Session
from database import SessionLocal

# Esta función es el "grifo" que abre y cierra la conexión
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Esta línea es vital: le dice a SQLAlchemy que cree la tabla ahora mismo
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Definimos el modelo de datos de un Libro
class Libro(BaseModel):
    id: int
    titulo: str
    autor: str
    disponible: bool = True
    activo: bool = True  # <--- Nuevo campo: True es visible, False es "borrado"

biblioteca = []

@app.get("/")
def inicio():
    return {"mensaje": "Bienvenido a la API de la Biblioteca"}

# 1. Obtener todos los libros o todos los libros de un autor
@app.get("/libros", response_model=List[Libro])
def obtener_libros(autor: Optional[str] = None, db: Session = Depends(get_db)):
    # 1. Creamos la consulta base: "Tráeme todos los LibroDB que estén activos"
    query = db.query(LibroDB).filter(LibroDB.activo == True)
    
    # 2. Si el usuario pasó un autor por la URL, filtramos la consulta
    if autor:
        # Usamos ilike para que no importe mayúsculas/minúsculas
        query = query.filter(LibroDB.autor.ilike(f"%{autor}%"))
        
    # 3. Ejecutamos la consulta y devolvemos los resultados
    libros_db = query.all()
    return libros_db

# 2. Obtener un libro por su ID
@app.get("/libros/{libro_id}")
def obtener_libro(libro_id: int):
    for libro in biblioteca:
        if libro["id"] == libro_id:
            return libro
    raise HTTPException(status_code=404, detail="Libro no encontrado")

# 3. Agregar un nuevo libro
@app.post("/libros", response_model=Libro)
def crear_libro(libro: Libro, db: Session = Depends(get_db)):
    # 1. Creamos el objeto para la base de datos usando los datos que llegan (Pydantic)
    nuevo_libro = LibroDB(
        id=libro.id,
        titulo=libro.titulo,
        autor=libro.autor,
        disponible=libro.disponible,
        activo=libro.activo
    )
    
    # 2. Le pedimos a SQLAlchemy que lo guarde
    db.add(nuevo_libro)
    db.commit()      # <--- Aquí se escribe físicamente en el archivo .db
    db.refresh(nuevo_libro) # <--- Recargamos el objeto para confirmar que se guardó
    
    return nuevo_libro

# 4. Desactivar un libro (borrado lógico)
@app.delete("/libros/{libro_id}")
def desactivar_libro(libro_id: int):
    for libro in biblioteca:
        if libro["id"] == libro_id:
            if not libro["activo"]:
                raise HTTPException(status_code=400, detail="El libro ya estaba desactivado")
            
            libro["activo"] = False  # <--- Aquí ocurre el "borrado lógico"
            return {"mensaje": f"El libro '{libro['titulo']}' ha sido marcado como inactivo"}
            
    raise HTTPException(status_code=404, detail="Libro no encontrado")

# 5. Actualizar un libro 
@app.put("/libros/{libro_id}")
def actualizar_libro(libro_id: int, libro_actualizado: Libro):
    for indice, libro in enumerate(biblioteca):
        if libro["id"] == libro_id:
            # Si el libro está desactivado (borrado lógico), no permitimos editarlo
            if not libro["activo"]:
                raise HTTPException(status_code=400, detail="No se puede editar un libro inactivo")
            
            # Reemplazamos los datos antiguos con los nuevos
            # Convertimos el objeto Pydantic a diccionario
            biblioteca[indice] = libro_actualizado.dict()
            return {"mensaje": f"Libro con ID {libro_id} actualizado correctamente"}
            
    raise HTTPException(status_code=404, detail="Libro no encontrado")

# 6 Lógica de Préstamo ---
@app.post("/libros/{libro_id}/prestar")
def prestar_libro(libro_id: int):
    for libro in biblioteca:
        if libro["id"] == libro_id:
            if not libro["activo"]:
                raise HTTPException(status_code=400, detail="El libro no existe en el catálogo activo")
            if not libro["disponible"]:
                raise HTTPException(status_code=400, detail="El libro ya se encuentra prestado")
            
            libro["disponible"] = False
            return {"mensaje": f"Has pedido prestado: {libro['titulo']}"}
            
    raise HTTPException(status_code=404, detail="Libro no encontrado")

# 7 Lógica de Devolución ---
@app.post("/libros/{libro_id}/devolver")
def devolver_libro(libro_id: int):
    for libro in biblioteca:
        if libro["id"] == libro_id:
            # Regla 1: No se puede devolver algo que no existe físicamente (borrado lógico)
            if not libro["activo"]:
                raise HTTPException(status_code=400, detail="El libro no pertenece al catálogo activo")
            
            # Regla 2: Si el libro ya está disponible, no tiene sentido devolverlo
            if libro["disponible"]:
                raise HTTPException(status_code=400, detail="El libro ya se encuentra en la biblioteca")
            
            # Acción: Cambiamos el estado a disponible
            libro["disponible"] = True
            return {"mensaje": f"Has devuelto el libro: {libro['titulo']}. ¡Gracias!"}
            
    raise HTTPException(status_code=404, detail="Libro no encontrado")


