# Biblioteca API con FastAPI

Este proyecto es una API RESTful desarrollada en **Python** para la gestión de una biblioteca. Implementa un ciclo de vida completo de datos (**CRUD**) y utiliza validación de tipos técnica mediante **Pydantic**.

## 🚀 Estado del Proyecto (v0.1.0)
- [x] CRUD básico en memoria.
- [x] Conexión a Base de Datos (SQLite).
- [x] Persistencia en creación (POST) y consulta (GET).
- [ ] Persistencia en actualización y borrado (Próximamente).

## 🛠️ Stack Tecnológico

* **Lenguaje:** Python 3.x
* **Framework:** [FastAPI](https://fastapi.tiangolo.com/)
* **Servidor ASGI:** Uvicorn
* **Modelado de datos:** Pydantic

## 🏁 Instalación y Ejecución

1. **Clonar el repositorio:**
   `git clone https://github.com/jbracho77/biblioteca-api-python.git`

2. **Instalar las librerías necesarias:**
   `pip install -r requirements.txt`

3. **Iniciar el servidor de desarrollo:**
   `uvicorn main:app --reload`

4. **Acceder a la documentación automática (Swagger UI):**
   `http://127.0.0.1:8000/docs`

## 🛠️ Notas de Desarrollo (Linux Mint)
Cada vez que abras una terminal nueva, debes activar el entorno:
`source env/bin/activate`
---


## 📝 Historial de Versiones (Changelog)

### [v0.1.0] - 2026-02-22
* **ESTRUCTURA:** Configuración de SQLAlchemy y creación de `database.py`.
* **PERSISTENCIA:** Implementación del modelo `LibroDB`.
* **BASE DE DATOS:** Generación automática del archivo `biblioteca.db` (SQLite).

### [v0.0.7] - 2026-02-22
* **AÑADIDO:** Parámetro de búsqueda por `titulo`.
* **MEJORA:** Capacidad de combinar múltiples filtros (autor + título) en una sola consulta.
* **MEJORA:** Normalización de texto para que las búsquedas no dependan de mayúsculas/minúsculas.

### [v0.0.6] - 2026-02-22
* **AÑADIDO:** Búsqueda avanzada de libros por autor.
* **MEJORA:** Implementación de Case-Insensitivity (ignora mayúsculas) en las búsquedas.
* **MEJORA:** Soporte para coincidencias parciales en los nombres de autores.

### [v0.0.5] - 2026-02-22
* **AÑADIDO:** Lógica de negocio para **Devoluciones** (`POST /libros/{id}/devolver`).
* **MEJORA:** Control de estados de disponibilidad (evita devolver libros ya disponibles).
* **LOGRO:** Sistema básico de gestión de flujo de inventario completado.

### [v0.0.4] - 2026-02-22
* **AÑADIDO:** Lógica de negocio para **Préstamos** (`POST /libros/{id}/prestar`).
* **MEJORA:** Validación de IDs únicos para evitar registros duplicados en la creación.
* **MEJORA:** Limpieza de strings (`.strip()`) en títulos para evitar datos vacíos.
* **SEGURIDAD:** Restricción de acciones (editar/prestar) sobre libros inactivos.

### [v0.0.3] - 2026-02-20
- **AÑADIDO:** Método `PUT` para la actualización completa de libros.
- **MEJORA:** Validación para impedir la edición de libros marcados como inactivos.
- **LOGRO:** Finalización del ciclo CRUD básico en memoria.

### [v0.0.2] - 2026-02-20
- **AÑADIDO:** Implementación de Borrado Lógico mediante el atributo "activo".
- **CAMBIADO:** El endpoint de lectura ahora filtra automáticamente los libros inactivos.
- **CORREGIDO:** Manejo de errores 404 para libros no encontrados.

### [v0.0.1] - 2026-02-20
- **AÑADIDO:** Estructura inicial del proyecto.
- **AÑADIDO:** Modelo de datos Pydantic y persistencia temporal en listas.
- **AÑADIDO:** Endpoints básicos de creación (`POST`) y lectura (`GET`).