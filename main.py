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

# Nuestra "base de datos" temporal (una lista)
biblioteca = [
    {"id": 1, "titulo": "Cien años de soledad", "autor": "Gabriel García Márquez", "disponible": True},
    {"id": 2, "titulo": "1984", "autor": "George Orwell", "disponible": False}
]

@app.get("/")
def inicio():
    return {"mensaje": "Bienvenido a la API de la Biblioteca"}

# 1. Obtener todos los libros
@app.get("/libros", response_model=List[Libro])
def obtener_libros():
    return biblioteca

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