from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta 
from ..database import get_db
from ..models import LibroDB
from ..schemas import Libro

router = APIRouter(
    prefix="/libros",
    tags=["Libros"]
)

@router.get("/", response_model=List[Libro])
def obtener_libros(
    titulo: Optional[str] = None, 
    autor: Optional[str] = None, 
    categoria: Optional[str] = None, # <-- Nuevo filtro
    solo_disponible: bool = False, 
    usuario: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(LibroDB).filter(LibroDB.activo == True)
    
    # Filtros existentes...
    if autor: query = query.filter(LibroDB.autor.ilike(f"%{autor}%"))
    if titulo: query = query.filter(LibroDB.titulo.ilike(f"%{titulo}%"))
    
    # NUEVO: Filtro por categoría
    if categoria:
        query = query.filter(LibroDB.categoria.ilike(f"%{categoria}%"))
        
    if solo_disponible: query = query.filter(LibroDB.disponible == True)
    if usuario: query = query.filter(LibroDB.usuario_prestamo.ilike(f"%{usuario}%"))
        
    return query.all()

# 8 Obtener los libros atrasados
@router.get("/reporte/atrasados", response_model=List[Libro])
def obtener_libros_atrasados(
    dias: int = Query(7, ge=1), # Por defecto 7 días, mínimo 1
    db: Session = Depends(get_db)
):
    # Calculamos la fecha límite (Hoy menos X días)
    fecha_limite = datetime.now() - timedelta(days=dias)
    
    # Buscamos libros que:
    # 1. No estén disponibles
    # 2. La fecha de préstamo sea ANTERIOR a la fecha límite
    # 3. Estén activos
    libros_en_mora = db.query(LibroDB).filter(
        LibroDB.disponible == False,
        LibroDB.fecha_prestamo <= fecha_limite,
        LibroDB.activo == True
    ).all()
    
    return libros_en_mora

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
def prestar_libro(
    libro_id: int, 
    # Validamos: mínimo 3 caracteres, máximo 50
    usuario: str = Query(..., min_length=3, max_length=50), 
    db: Session = Depends(get_db)
):
    libro = db.query(LibroDB).filter(LibroDB.id == libro_id, LibroDB.activo == True).first()
    
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
        
    if not libro.disponible:
        # Un toque de elegancia: decir quién lo tiene
        quien = libro.usuario_prestamo or "alguien"
        raise HTTPException(
            status_code=400, 
            detail=f"El libro ya lo tiene {quien}"
        )
    
    # Si pasa las validaciones, procedemos
    libro.disponible = False
    libro.fecha_prestamo = datetime.now()
    libro.usuario_prestamo = usuario
    db.commit()
    
    return {"mensaje": f"Libro '{libro.titulo}' prestado exitosamente a {usuario}"}

# 7 Lógica de Devolución ---
@router.post("/{libro_id}/devolver")
def devolver_libro(libro_id: int, db: Session = Depends(get_db)):
    libro = db.query(LibroDB).filter(LibroDB.id == libro_id, LibroDB.activo == True).first()
    
    if not libro:
        raise HTTPException(status_code=404, detail="No encontrado")
    
    # Al devolver, limpiamos ambos campos
    libro.disponible = True
    libro.fecha_prestamo = None
    libro.usuario_prestamo = None # <-- Limpiamos el deudor
    db.commit()
    
    return {"mensaje": f"Libro '{libro.titulo}' devuelto y disponible"}






