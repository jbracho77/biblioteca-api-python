# 📚 Biblioteca API - v0.0.2 (Alpha)

Este es el inicio de mi proyecto de API para gestión de bibliotecas, desarrollado con **FastAPI**.

## 🚀 Funcionalidades actuales
- [x] Listar todos los libros.
- [x] Buscar un libro por ID.
- [x] Agregar nuevos libros con validación de datos mediante **Pydantic**.

## 🛠️ Tecnologías utilizadas
- Python 3.x
- FastAPI
- Uvicorn (Servidor ASGI)

## 🏁 Cómo ejecutar
1. Instalar dependencias: `pip install -r requirements.txt`
2. Correr el servidor: `uvicorn main:app --reload`

## 📝 Historial de Versiones

### [v0.0.2] - 2026-02-20
**Añadido:**
- Implementación de **Borrado Lógico** (Soft Delete) mediante el atributo `activo`.
- Endpoint `DELETE /libros/{id}` para desactivar registros sin borrarlos físicamente.
- Filtro en `GET /libros` para mostrar únicamente libros activos.

**Cambiado:**
- El modelo de datos `Libro` ahora incluye el campo `activo: bool`.

---

### [v0.0.1] - 2026-02-20
- Estructura inicial con FastAPI.
- Endpoints básicos de lectura (`GET`) y creación (`POST`).
- Persistencia temporal en memoria (Listas).