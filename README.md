# Wetransfer API – Sistema de transferencia de archivos con expiración automática

## Descripción general
Este proyecto consiste en el desarrollo de una API REST utilizando FastAPI, la cual permite la gestión de archivos mediante un sistema de subida, almacenamiento y descarga segura a través de tokens únicos. Cada archivo cuenta con un tiempo de expiración, lo que permite que el sistema elimine automáticamente la información cuando ya no es válida.

El objetivo principal del proyecto es simular el funcionamiento básico de un servicio tipo transferencia de archivos, aplicando conceptos de backend, bases de datos relacionales, manejo de archivos en servidor y procesos automáticos en segundo plano.

## Objetivo del sistema
Diseñar e implementar una API que permita:
- Subir archivos al servidor
- Generar un identificador único (token) para descarga
- Controlar la validez de los archivos mediante expiración
- Eliminar archivos automáticamente una vez vencido su tiempo de vida
- Mantener sincronización entre sistema de archivos y base de datos

## Tecnologías utilizadas
- Python 3.12
- FastAPI
- PostgreSQL
- SQLAlchemy
- Uvicorn
- asyncio

## Arquitectura del proyecto

app/
├── main.py
├── routes/
│   └── file_routes.py
├── database/
│   └── connection.py
├── tasks/
│   └── background_tasks.py
uploads/

## Base de datos

Se utiliza PostgreSQL con una tabla principal llamada `files`, la cual almacena la información de cada archivo.

Campos principales:
- id
- filename
- stored_name
- file_size
- mime_type
- token
- expires_at
- status

## Funcionalidades del sistema

### Subida de archivos
- Subida de archivos al servidor
- Generación de nombre único
- Generación de token
- Asignación de expiración

### Descarga segura por token
http://127.0.0.1:8000/download/{token}

Validaciones:
- Existencia en base de datos
- Estado activo
- No expirado
- Existencia física del archivo

Entrega mediante FileResponse.

### Limpieza automática de archivos
- Ejecución en segundo plano al iniciar el servidor
- Revisión periódica de archivos expirados
- Actualización de estado en base de datos
- Eliminación de archivos físicos

## Ejecución del proyecto

venv\Scripts\activate
uvicorn app.main:app --reload
http://127.0.0.1:8000/docs

## Conclusión
Proyecto backend con FastAPI que implementa gestión de archivos con expiración automática, validación por token y limpieza en segundo plano usando asyncio.


