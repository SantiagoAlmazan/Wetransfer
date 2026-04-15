# Wetransfer API – Sistema de transferencia de archivos

## Descripción del proyecto
Este proyecto consiste en una API desarrollada con FastAPI que permite subir, almacenar y descargar archivos mediante un sistema de tokens. La idea principal es simular un servicio tipo transferencia de archivos, donde cada archivo tiene un tiempo de vida y después de cierto tiempo deja de estar disponible.

Durante el desarrollo se trabajó con conceptos de backend, bases de datos y procesos automáticos para limpieza de información.

---

## Objetivo del sistema
El objetivo de este proyecto es construir una API funcional que permita:

- Subir archivos al servidor
- Generar un token único para cada archivo
- Permitir la descarga mediante ese token
- Controlar la expiración de los archivos
- Eliminar automáticamente archivos que ya vencieron
- Mantener sincronizada la base de datos con los archivos reales del servidor

---

## Tecnologías utilizadas
- Python 3.12
- FastAPI
- PostgreSQL
- SQLAlchemy
- Uvicorn
- asyncio

---

## Estructura del proyecto
El proyecto está organizado de forma sencilla para mantenerlo entendible:
app/
├── main.py
├── routes/
│ └── file_routes.py
├── database/
│ └── connection.py
├── tasks/
│ └── background_tasks.py
uploads/


---

## Base de datos
Se utiliza PostgreSQL con una tabla llamada `files`, donde se guarda la información de cada archivo.

Campos principales:
- id
- filename
- stored_name
- file_size
- mime_type
- token
- expires_at
- status

---

## Funcionalidades principales

### Subida de archivos
Cuando se sube un archivo:
- Se guarda en el servidor
- Se genera un nombre único
- Se crea un token para poder descargarlo después
- Se define un tiempo de expiración

---

### Descarga de archivos
Los archivos se descargan usando una URL como esta:
GET /download/{token}


Antes de entregar el archivo, el sistema revisa:
- Que el archivo exista en la base de datos
- Que esté activo
- Que no haya expirado
- Que exista físicamente en el servidor

---

### Limpieza automática
El sistema también incluye un proceso automático que se ejecuta en segundo plano. Este proceso:

- Revisa archivos expirados cada cierto tiempo
- Cambia su estado en la base de datos
- Elimina los archivos del servidor
- Mantiene el sistema limpio sin intervención manual

---

## Ejecución del proyecto

Para ejecutar el proyecto:

```bash
venv\Scripts\activate
uvicorn app.main:app --reload


Luego se puede probar desde:

http://127.0.0.1:8000/docs

Lo que más me costó del proyecto

Lo más complicado fue conectar correctamente la base de datos con FastAPI y entender bien cómo manejar los imports entre módulos. Al inicio tuve varios errores que no dejaban correr el proyecto, pero poco a poco se fue corrigiendo hasta que todo funcionó de forma estable.

También fue un reto implementar la limpieza automática de archivos, ya que requiere que el sistema se mantenga corriendo en segundo plano sin afectar la API.

## Lo que aprendí

Con este proyecto aprendí a estructurar mejor una API en Python, a manejar bases de datos relacionales con SQLAlchemy y a implementar procesos automáticos para mantenimiento del sistema.

También entendí mejor cómo se organiza un backend real y la importancia de mantener un código ordenado para evitar errores.

## Conclusión

Este proyecto me ayudó a reforzar conocimientos de backend, especialmente en APIs, bases de datos y manejo de archivos. Aunque tuvo errores al inicio, el proceso de depuración fue clave para entender mejor

