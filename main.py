from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI()

# Definimos el modelo de datos de un Libro
class Libro(BaseModel):
    id: int
    titulo: str
    autor: str
    disponible: bool = True
    activo: bool = True  # <--- Nuevo campo: True es visible, False es "borrado"

biblioteca = [
    {"id": 1, "titulo": "Cien años de soledad", "autor": "García Márquez", "disponible": True, "activo": True},
    {"id": 2, "titulo": "1984", "autor": "George Orwell", "disponible": False, "activo": True}
]

@app.get("/")
def inicio():
    return {"mensaje": "Bienvenido a la API de la Biblioteca"}

# 1. Obtener todos los libros
@app.get("/libros", response_model=List[Libro])
def obtener_libros():
    # Usamos una "list comprehension" para filtrar
    libros_activos = [libro for libro in biblioteca if libro["activo"] == True]
    return libros_activos

# 2. Obtener un libro por su ID
@app.get("/libros/{libro_id}")
def obtener_libro(libro_id: int):
    for libro in biblioteca:
        if libro["id"] == libro_id:
            return libro
    raise HTTPException(status_code=404, detail="Libro no encontrado")

# 3. Agregar un nuevo libro
# --- Mejora 1: Validación al crear ---
@app.post("/libros")
def crear_libro(nuevo_libro: Libro):
    # Comprobamos si el ID ya existe
    for libro in biblioteca:
        if libro["id"] == nuevo_libro.id:
            raise HTTPException(status_code=400, detail="El ID del libro ya existe")
    
    # Comprobamos que el título no esté vacío
    if not nuevo_libro.titulo.strip():
        raise HTTPException(status_code=400, detail="El título no puede estar vacío")

    biblioteca.append(nuevo_libro.dict())
    return {"mensaje": f"Libro '{nuevo_libro.titulo}' registrado"}

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


