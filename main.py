from fastapi import FastAPI
from app.database import engine, Base
from app.routers import libros

# Crear las tablas en la DB
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mi Biblioteca API")

# Incluir las rutas
app.include_router(libros.router)

@app.get("/")
def home():
    return {"mensaje": "Bienvenido a la API de la Biblioteca"}