# Variables de entorno — EquipManager

Copia `.env.example` a `.env` y completa los valores antes de correr el proyecto.

```bash
cp .env.example .env
```

---

## Variables actuales

| Variable | Ejemplo | Requerida | Descripción |
|----------|---------|-----------|-------------|
| `SECRET_KEY` | `django-insecure-...` | ✅ Sí | Clave secreta de Django. Nunca exponerla ni subirla al repositorio. Generar una nueva con `python -m django startproject` o con `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"` |
| `DEBUG` | `True` / `False` | ✅ Sí | `True` en desarrollo, `False` obligatorio en producción |
| `DATABASE_URL` | `sqlite:///db.sqlite3` | ✅ Sí | Cadena de conexión a la base de datos. SQLite para desarrollo, PostgreSQL para producción |

---

## Variables a agregar durante el desarrollo

Estas variables no existen todavía pero serán necesarias conforme avance el proyecto:

| Variable | Ejemplo | Módulo | Descripción |
|----------|---------|--------|-------------|
| `EMAIL_HOST` | `smtp.gmail.com` | Notificaciones | Servidor SMTP para envío de correos |
| `EMAIL_PORT` | `587` | Notificaciones | Puerto del servidor SMTP |
| `EMAIL_HOST_USER` | `sistema@empresa.com` | Notificaciones | Correo remitente |
| `EMAIL_HOST_PASSWORD` | `app_password_aqui` | Notificaciones | Contraseña o app password del correo |
| `EMAIL_USE_TLS` | `True` | Notificaciones | Activar TLS en la conexión SMTP |
| `ALLOWED_HOSTS` | `localhost,127.0.0.1` | Seguridad | Hosts permitidos, requerido cuando `DEBUG=False` |

---

## Cadenas de conexión según entorno

**Desarrollo (SQLite)**
```
DATABASE_URL=sqlite:///db.sqlite3
```

**Producción (PostgreSQL)**
```
DATABASE_URL=postgres://usuario:contraseña@host:5432/nombre_db
```

---

## Cómo generar una SECRET_KEY segura

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
