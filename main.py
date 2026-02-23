from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
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
    # min_length: mínimo de caracteres | max_length: máximo
    titulo: str = Field(..., min_length=1, max_length=100, description="El título no puede estar vacío")
    autor: str = Field(..., min_length=3, max_length=50, description="El nombre del autor debe tener al menos 3 caracteres")
    disponible: bool = True
    activo: bool = True

    class Config:
        from_attributes = True

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
@app.get("/libros/{libro_id}", response_model=Libro)
def obtener_libro_por_id(libro_id: int, db: Session = Depends(get_db)):
    libro = db.query(LibroDB).filter(LibroDB.id == libro_id, LibroDB.activo == True).first()
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return libro

# 3. Agregar un nuevo libro
@app.post("/libros", response_model=Libro)
def crear_libro(libro: Libro, db: Session = Depends(get_db)):
    # 1. BUSCAR si el ID ya existe en la base de datos
    existe = db.query(LibroDB).filter(LibroDB.id == libro.id).first()
    
    if existe:
        # Si existe, lanzamos un error 400 (Bad Request)
        raise HTTPException(
            status_code=400, 
            detail=f"Error: Ya existe un libro con el ID {libro.id}. Intenta con otro."
        )

    # 2. Si no existe, procedemos a crear el objeto
    nuevo_libro = LibroDB(
        id=libro.id,
        titulo=libro.titulo,
        autor=libro.autor,
        disponible=libro.disponible,
        activo=libro.activo
    )
    
    db.add(nuevo_libro)
    db.commit()
    db.refresh(nuevo_libro)
    
    return nuevo_libro

# 4. Desactivar un libro (borrado lógico)
@app.delete("/libros/{libro_id}")
def eliminar_libro(libro_id: int, db: Session = Depends(get_db)):
    # 1. Buscar el libro en la base de datos
    libro_db = db.query(LibroDB).filter(LibroDB.id == libro_id, LibroDB.activo == True).first()
    
    # 2. Si no existe, lanzar error 404
    if not libro_db:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    
    # 3. Borrado lógico: lo marcamos como no activo
    libro_db.activo = False
    
    # 4. Guardar cambios
    db.commit()
    
    return {"message": f"Libro con ID {libro_id} eliminado correctamente (lógico)"}

# 5. Actualizar un libro 
@app.put("/libros/{libro_id}", response_model=Libro)
def actualizar_libro(libro_id: int, libro_actualizado: Libro, db: Session = Depends(get_db)):
    # 1. Buscar el libro existente
    libro_db = db.query(LibroDB).filter(LibroDB.id == libro_id, LibroDB.activo == True).first()
    
    if not libro_db:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    
    # 2. Actualizar los campos
    libro_db.titulo = libro_actualizado.titulo
    libro_db.autor = libro_actualizado.autor
    libro_db.disponible = libro_actualizado.disponible
    
    # 3. Guardar en la base de datos
    db.commit()
    db.refresh(libro_db)
    
    return libro_db

# 6 Lógica de Préstamo ---
@app.post("/libros/{libro_id}/prestar")
def prestar_libro(libro_id: int, db: Session = Depends(get_db)):
    libro = db.query(LibroDB).filter(LibroDB.id == libro_id, LibroDB.activo == True).first()
    
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    if not libro.disponible:
        raise HTTPException(status_code=400, detail="El libro ya está prestado")
    
    libro.disponible = False
    db.commit()
    return {"message": f"Has pedido prestado: {libro.titulo}"}

# 7 Lógica de Devolución ---
@app.post("/libros/{libro_id}/devolver")
def devolver_libro(libro_id: int, db: Session = Depends(get_db)):
    libro = db.query(LibroDB).filter(LibroDB.id == libro_id, LibroDB.activo == True).first()
    
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    
    libro.disponible = True
    db.commit()
    return {"message": f"Has devuelto: {libro.titulo}. ¡Gracias!"}


