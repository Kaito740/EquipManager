# EquipManager

> ✅ Completado

REST API para la gestión de activos tecnológicos de una empresa — cubre el ciclo completo de entrega de equipos, mantenimientos y devoluciones, con generación automática de actas y notificaciones por correo.

## El problema

El área de Sistemas de una empresa gestionaba todos sus equipos electrónicos — laptops, monitores, teclados, mouses, UPS, impresoras — completamente en Excel.

Cada vez que un empleado recibía o devolvía un equipo, el técnico abría una plantilla, copiaba el archivo, llenaba los datos a mano y lo guardaba como acta. Si un equipo iba a mantenimiento, a veces se generaba acta, a veces no — dependía del técnico del día. El inventario del almacén se manejaba con cajas físicas y memoria humana: para saber si había laptops disponibles había que ir físicamente o preguntarle al jefe.

Esto generaba problemas concretos:

- **Sin historial:** si a una laptop le cambiaban el disco duro, el acta original seguía diciendo el disco viejo.
- **Sin evidencia de estado:** cuando un equipo volvía dañado, nadie podía probar si el daño existía antes de la entrega o lo causó el usuario.
- **Sin trazabilidad:** los códigos patrimoniales existían, pero nadie sabía en tiempo real dónde estaba cada bien ni en qué estado.
- **Inventario ciego:** para ubicar un equipo específico había que revisar cada archivo de Excel uno por uno.

## La solución

EquipManager reemplaza ese proceso manual con una API que registra cada movimiento, genera actas automáticamente en PDF listas para imprimir y firmar, y permite saber en cualquier momento dónde está cada equipo y en qué estado.

## Stack

- **Backend:** Django 6.0 + Django REST Framework
- **Autenticación:** JWT (djangorestframework-simplejwt)
- **Base de datos:** SQLite (desarrollo) / PostgreSQL (producción)
- **Generación de PDFs:** ReportLab
- **Documentación API:** drf-yasg (Swagger/OpenAPI)
- **Filtros:** django-filter
- **Testing:** pytest + pytest-django

## Requisitos previos

- Python 3.12 o superior (solo instalación local)
- Git
- Docker + Docker Compose (opcional)

### Instalación de Docker

**Windows:**

1. Descarga Docker Desktop desde https://www.docker.com/products/docker-desktop
2. Ejecuta el instalador y sigue las instrucciones
3. Inicia Docker Desktop

**Mac:**

1. Descarga Docker Desktop desde https://www.docker.com/products/docker-desktop
2. Arrastra Docker a tu carpeta de Aplicaciones
3. Abre Docker Desktop

**Linux (Ubuntu/Debian):**

```bash
sudo apt update
sudo apt install docker.io docker-compose
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER
```

Cierra sesión y vuelve a entrar para aplicar el cambio de grupo.

## Instalación con Docker (recomendado)

**1. Clonar el repositorio**

```bash
git clone https://github.com/Kaito740/EquipManager.git
cd EquipManager
```

**2. Iniciar los servicios**

```bash
docker-compose up --build
```

La API estará disponible en `http://localhost:8000/`

## Instalación local (sin Docker)

**1. Clonar el repositorio**

```bash
git clone https://github.com/Kaito740/EquipManager.git
cd EquipManager
```

**2. Crear y activar el entorno virtual**

```bash
python -m venv .venv
```

Windows:
```powershell
& .venv\Scripts\Activate.ps1
```

Mac/Linux:
```bash
source .venv/bin/activate
```

**3. Instalar dependencias**

```bash
pip install -r requirements.txt
```

**4. Configurar variables de entorno**

Copia `.env.example` a `.env` y completa los valores:

```bash
cp .env.example .env
```

**5. Aplicar migraciones**

```bash
python manage.py migrate
```

**6. Crear superusuario**

```bash
python manage.py createsuperuser
```

**7. Correr el servidor**

```bash
python manage.py runserver
```

La API estará disponible en `http://127.0.0.1:8000/`


## Testing

```bash
pytest
```

Con detalle:

```bash
pytest -v
```

## Licencia

MIT

## Documentación

- [Arquitectura del sistema](docs/architecture.md) — Flujos, estados de equipos y arquitectura en capas
- [Modelo de datos](docs/database.md) — Diagrama ER y descripción de tablas
- [Autenticación y permisos](docs/authentication.md) — Flujo JWT y sistema de grupos de Django
- [Decisiones técnicas](docs/decisions.md) — Por qué se eligió cada tecnología y patrón
- [Variables de entorno](docs/environment.md) — Configuración del proyecto
- [Referencia de la API](https://equipmanager.ddns.net/swagger/) — Swagger UI con todos los endpoints