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
@app.post("/libros")
def crear_libro(nuevo_libro: Libro):
    biblioteca.append(nuevo_libro.dict())
    return {"mensaje": f"Libro '{nuevo_libro.titulo}' agregado con éxito"}

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