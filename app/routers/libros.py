from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from ..models import LibroDB
from ..schemas import Libro

router = APIRouter(
    prefix="/libros",
    tags=["Libros"]
)

@router.get("/", response_model=List[Libro]) # Nota que ahora la ruta es "/" porque el prefijo es "/libros"
def obtener_libros(
    titulo: Optional[str] = None, 
    autor: Optional[str] = None, 
    solo_disponible: bool = False, 
    db: Session = Depends(get_db)
):
    query = db.query(LibroDB).filter(LibroDB.activo == True)
    if autor:
        query = query.filter(LibroDB.autor.ilike(f"%{autor}%"))
    if titulo:
        query = query.filter(LibroDB.titulo.ilike(f"%{titulo}%"))
    if solo_disponible:
        query = query.filter(LibroDB.disponible == True)   
    return query.all()

# 2. Obtener un libro por su ID
@router.get("/{libro_id}", response_model=Libro)
def obtener_libro_por_id(libro_id: int, db: Session = Depends(get_db)):
    libro = db.query(LibroDB).filter(LibroDB.id == libro_id, LibroDB.activo == True).first()
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return libro

# 3. Agregar un nuevo libro
@router.post("/", response_model=Libro)
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
@router.delete("/{libro_id}")
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
@router.put("/{libro_id}", response_model=Libro)
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
@router.post("/{libro_id}/prestar")
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
@router.post("/{libro_id}/devolver")
def devolver_libro(libro_id: int, db: Session = Depends(get_db)):
    libro = db.query(LibroDB).filter(LibroDB.id == libro_id, LibroDB.activo == True).first()
    
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    
    libro.disponible = True
    db.commit()
    return {"message": f"Has devuelto: {libro.titulo}. ¡Gracias!"}


