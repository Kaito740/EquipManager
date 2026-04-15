# Variables de entorno — EquipManager

Copia `.env.example` a `.env` y completa los valores antes de correr el proyecto.

```bash
cp .env.example .env
```

---

## Variables actuales

| Variable | Ejemplo | Requerida | Descripción |
|----------|---------|-----------|-------------|
| `SECRET_KEY` | `django-insecure-...` | ✅ Sí | Clave secreta de Django. Nunca exponerla ni subirla al repositorio. Generar una nueva con `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"` |
| `DEBUG` | `True` / `False` | ✅ Sí | `True` en desarrollo, `False` obligatorio en producción |
| `DATABASE_URL` | `sqlite:///db.sqlite3` | ✅ Sí | Cadena de conexión a la base de datos. SQLite para desarrollo, PostgreSQL para producción |
| `ALLOWED_HOSTS` | `localhost,127.0.0.1` | Solo prod | Hosts permitidos, requerido cuando `DEBUG=False` |
| `CORS_ALLOW_ALL_ORIGINS` | `True` / `False` | ✅ Sí | `True` en desarrollo permite cualquier origen. `False` en producción — configurar `CORS_ALLOWED_ORIGINS` con los dominios permitidos |

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
