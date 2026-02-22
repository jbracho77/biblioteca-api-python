# Biblioteca API con FastAPI

Este proyecto es una API RESTful desarrollada en **Python** para la gestión de una biblioteca. Implementa un ciclo de vida completo de datos (**CRUD**) y utiliza validación de tipos técnica mediante **Pydantic**.

## 🚀 Funcionalidades (CRUD)

* **[C] Create:** Registro de nuevos libros con validación de tipos (`int`, `str`, `bool`).
* **[R] Read:** Consulta de la lista de libros y búsqueda específica por **ID**.
* **[U] Update:** Actualización de información de libros existentes mediante el método **PUT**.
* **[D] Delete:** Implementación de **Borrado Lógico** (*Soft Delete*) para preservar el historial de datos.
* **[P] Business Logic:** Endpoint especial para la **gestión de préstamos**, controlando la disponibilidad en tiempo real.

## 🛠️ Stack Tecnológico

* **Lenguaje:** Python 3.x
* **Framework:** [FastAPI](https://fastapi.tiangolo.com/)
* **Servidor ASGI:** Uvicorn
* **Modelado de datos:** Pydantic

## 🏁 Instalación y Ejecución

1. **Clonar el repositorio:**
   `git clone https://github.com/tu-usuario/nombre-del-repo.git`

2. **Instalar las librerías necesarias:**
   `pip install -r requirements.txt`

3. **Iniciar el servidor de desarrollo:**
   `uvicorn main:app --reload`

4. **Acceder a la documentación automática (Swagger UI):**
   `http://127.0.0.1:8000/docs`

---

## 📝 Historial de Versiones (Changelog)

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