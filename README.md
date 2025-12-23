FastAPI tutorial app with JWT auth (FastAPI Users), SQLite, and ImageKit uploads.

## Requisitos
- Python 3.12
- [uv](https://docs.astral.sh/uv/) instalado (o `pip`/`venv` estándar)
- Variables de entorno en `.env`:
  - `SECRET=<jwt_secret>`
  - `IMAGEKIT_PUBLIC_KEY=...`
  - `IMAGEKIT_PRIVATE_KEY=...`
  - `IMAGEKIT_URL=...`

## Instalación
```bash
uv sync
```

## Ejecución
```bash
uv run uvicorn app.app:app --reload --host 0.0.0.0 --port 8000
```
Documentación interactiva: http://localhost:8000/docs

## Flujo de autenticación
1) Registrar usuario: `POST /auth/register` con `email` y `password`.
2) Login: `POST /auth/jwt/login` con las mismas credenciales.
3) Usa el `access_token` devuelto en el header `Authorization: Bearer <token>` para las rutas protegidas.

## Rutas principales
- `POST /auth/register` – alta de usuario.
- `POST /auth/jwt/login` – login y obtención de JWT.
- `POST /upload` – requiere JWT; recibe `file` (UploadFile) y `caption`; sube a ImageKit y guarda en DB.
- `GET /feed` – requiere JWT; lista posts más recientes.
- `DELETE /posts/{post_id}` – requiere JWT; elimina post por id.

## Base de datos
- SQLite en `test.db` usando SQLAlchemy async.
- Si cambias el modelo y da error de columnas faltantes, borra `test.db` y deja que se regenere al arrancar.

## Notas de desarrollo
- Los usuarios y posts se relacionan por `user_id` (UUID) manejado por FastAPI Users.
- Las rutas protegidas usan `current_active_user`; asegúrate de enviar el token JWT.
