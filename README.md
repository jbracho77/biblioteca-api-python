# Biblioteca API con FastAPI

Este proyecto es una API RESTful desarrollada en **Python** para la gestión de una biblioteca. Implementa un ciclo de vida completo de datos (**CRUD**) y utiliza validación de tipos técnica mediante **Pydantic**.

## 🛡️ Capa de Validación (v0.3.2)
Hemos reforzado la seguridad de los datos en los préstamos:

- **Identidad Obligatoria**: No se permiten préstamos anónimos.
- **Restricciones de Nombre**: El nombre del usuario debe tener entre 3 y 50 caracteres.
- **Mensajes Informativos**: Si un libro ya está prestado, la API informa quién es el deudor actual.

## 👥 Control de Usuarios (v0.3.1)
Ahora el sistema identifica quién tiene cada ejemplar:

- **Asignación de préstamos**: El endpoint `/prestar` ahora requiere un nombre de usuario.
- **Auditoría de deudores**: Campo `usuario_prestamo` añadido para trazabilidad completa.
- **Búsqueda por usuario**: Nuevo filtro en `GET /libros?usuario=nombre` para consultar qué libros tiene una persona específica.

## 🕒 Gestión de Tiempos (v0.3.0)
El sistema ahora registra el ciclo de vida de los préstamos con precisión temporal:

- **Registro de actividad**: Se almacena automáticamente la fecha y hora exacta (`YYYY-MM-DD HH:MM:SS`) al momento de realizar un préstamo.
- **Trazabilidad**: El campo `fecha_prestamo` permite auditar cuánto tiempo ha estado un libro fuera de la biblioteca.
- **Limpieza de estados**: Al devolver un libro, la marca de tiempo se reinicia (`null`), dejando el ejemplar listo para un nuevo ciclo.

## 🛠️ Nuevos Endpoints de Gestión
- `POST /libros/{id}/prestar`: Cambia el estado a no disponible y sella la fecha actual.
- `POST /libros/{id}/devolver`: Restablece la disponibilidad y limpia el registro de fecha.

## 📊 Ejemplo de Respuesta (JSON)
```json
{
  "id": 1,
  "titulo": "El resplandor",
  "autor": "Stephen King",
  "disponible": false,
  "fecha_prestamo": "2026-02-23T13:22:40"
}
```

## 🏗️ Arquitectura del Proyecto (v0.2.0)
El proyecto ha sido refactorizado siguiendo una arquitectura modular para mejorar la escalabilidad:

- **`app/database.py`**: Configuración y conexión a SQLAlchemy.
- **`app/models.py`**: Definición de tablas de la base de datos (SQLAlchemy).
- **`app/schemas.py`**: Modelos de validación y contratos de datos (Pydantic).
- **`app/routers/`**: Lógica de los endpoints organizada por módulos.
- **`main.py`**: Punto de entrada de la aplicación.

## 🚀 Estado del Proyecto (v0.1.2)
- [x] **Persistencia total**: Uso de SQLite y SQLAlchemy.
- [x] **Validaciones robustas**: Control de IDs duplicados y restricciones de texto con Pydantic.
- [x] **Búsqueda Avanzada**: Filtros por título (palabras clave), autor y disponibilidad.
- [x] **Borrado Lógico**: Los libros no se eliminan físicamente, se marcan como inactivos.

## 🛠️ Nuevas Funcionalidades de Consulta
Ahora puedes filtrar los libros usando parámetros en la URL o desde `/docs`:

* **Por Título:** `GET /libros?titulo=quijote` (Busca coincidencias parciales).
* **Por Autor:** `GET /libros?autor=cervantes`.
* **Solo Disponibles:** `GET /libros?solo_disponible=true` (Filtra los libros que no están prestados).
* **Combinado:** `GET /libros?titulo=viento&solo_disponible=true`.

## 🛡️ Reglas de Validación
- **ID**: Debe ser único (evita colisiones en la BD).
- **Título**: Obligatorio, mínimo 1 carácter, máximo 100.
- **Autor**: Obligatorio, mínimo 3 caracteres, máximo 50.

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

## 🛠️ Notas de Desarrollo (Linux Mint) ##
Cada vez que abras una terminal nueva, debes activar el entorno:
`source env/bin/activate`
---


## 📝 Historial de Versiones (Changelog)

### [v0.1.1] - 2026-02-22
* **MEJORA:** Validaciones de datos y manejo de errores.

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