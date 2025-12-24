FastAPI + FastAPI Users + Streamlit + ImageKit
===============================================

Backend FastAPI con autenticación JWT (FastAPI Users), SQLite async y subida de media a ImageKit. Frontend mínimo en Streamlit para probar login/registro, subir posts y ver/borrar tu contenido.

Contenido
---------
- Requisitos
- Configuración (.env)
- Instalación
- Ejecutar backend
- Ejecutar frontend
- Flujo de autenticación
- Endpoints clave
- Notas de base de datos
- Tips y solución de problemas

Requisitos
----------
- Python 3.12
- [uv](https://docs.astral.sh/uv/) instalado (o usa `pip`/`venv`)
- Dependencias en `pyproject.toml`

Configuración (.env)
--------------------
```
SECRET=<jwt_secret>
IMAGEKIT_PUBLIC_KEY=...
IMAGEKIT_PRIVATE_KEY=...
IMAGEKIT_URL=...
```

Instalación
-----------
```bash
uv sync
```

Ejecutar backend
----------------
```bash
uv run uvicorn app.app:app --reload --host 0.0.0.0 --port 8000
```
Docs: http://localhost:8000/docs

Ejecutar frontend (Streamlit)
-----------------------------
```bash
uv run streamlit run app/frontend.py
```
Espera la API en `http://localhost:8000`.

Flujo de autenticación
----------------------
1) POST `/auth/register` con `email` y `password`.
2) POST `/auth/jwt/login` con las mismas credenciales.
3) Usa el `access_token` en `Authorization: Bearer <token>` para rutas protegidas.

Frontend Streamlit
------------------
- Pantalla inicial: elegir Login o Registro.
- Tras autenticarse: subir posts y ver feed.
- Feed en columna: imagen/video embebido, caption, metadatos. Icono de basura solo en tus posts; llama a `DELETE /posts/{id}`.

Endpoints clave
---------------
- `POST /auth/register` – crear usuario.
- `POST /auth/jwt/login` – obtener JWT.
- `POST /upload` – requiere JWT; `file` + `caption`; sube a ImageKit y guarda en DB.
- `GET /feed` – requiere JWT; lista posts recientes.
- `DELETE /posts/{post_id}` – requiere JWT; solo dueño puede borrar.

Notas de base de datos
----------------------
- SQLite en `test.db` con SQLAlchemy async.
- Si cambias el modelo y faltan columnas, borra `test.db` y arranca de nuevo para recrear tablas.

Tips y solución de problemas
----------------------------
- 401 en `/upload` o `/feed`: falta token o expiró; reloguea en `/auth/jwt/login`.
- Errores de schema (columnas faltantes): borra `test.db`.
- Streamlit sin `watchdog`: usa `pip install watchdog` (opcional para recarga rápida).
