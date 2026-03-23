# Diseño del sistema — EquipManager

## El problema

El área de Sistemas manejaba equipos electrónicos completamente en Excel. Cada acta era un archivo separado, no había historial, no había trazabilidad, no había inventario en tiempo real.

## La solución

Una REST API con tres flujos principales que reemplaza el proceso manual por uno digital, trazable y con evidencia en actas generadas automáticamente.

---

## Flujo 1 — Entrega de equipos

```mermaid
flowchart TD
    A([Inicio: Nueva entrega]) --> B[Seleccionar empleado]
    B --> C[Agregar equipos por serie o codigo]
    C --> D{Agregar mas equipos?}
    D -->|Si| C
    D -->|No| E[Desplegar checklist por equipo]
    E --> F[Tecnico responde checklist]
    F --> G{Todos los equipos con checklist completo?}
    G -->|No| E
    G -->|Si| H[Confirmar entrega]
    H --> I[Transaccion: acta + estado ENTREGADO]
    I --> J([Fin])
```

## Flujo 2 — Mantenimiento

```mermaid
flowchart TD
    A([Inicio]) --> B{Origen?}
    B -->|Preventivo| C[Equipo desde almacen]
    B -->|Correctivo| D[Equipo entregado]
    C --> E[Equipo pasa a EN_MANTENIMIENTO]
    D --> E
    E --> F[Registrar trabajo: texto + componentes]
    F --> G[Responder checklist post-mantenimiento]
    G --> H[Cerrar ticket]
    H --> I[Transaccion: acta + cambia estado]
    I --> J([Fin])
```

**Regla crítica:** sin ticket cerrado con descripción, el sistema no permite cambiar el estado del equipo.

## Flujo 3 — Devolución

```mermaid
flowchart TD
    A([Inicio: Empleado devuelve equipos]) --> B[Tecnico marca estado de cada equipo]
    B --> C{Estado del equipo?}
    C -->|Conforme| D[Estado DISPONIBLE]
    C -->|Incidencia leve| E[Registrar incidencia LEVE]
    E --> F[Estado EN_MANTENIMIENTO]
    C -->|Incidencia grave| G[Registrar incidencia GRAVE]
    G --> H[Estado DADO_DE_BAJA]
    C -->|No devuelto| I[Registrar incidencia con descripcion]
    I --> J[Estado PERDIDO]
    D --> K{Mas equipos?}
    F --> K
    H --> K
    J --> K
    K -->|Si| B
    K -->|No| L[Confirmar devolucion]
    L --> M[Transaccion: acta + actualiza estados]
    M --> N([Fin])
```

---

## Arquitectura en capas

El proyecto usa una arquitectura en capas. Cada capa tiene una responsabilidad única y no se mezcla con las demás.

```mermaid
flowchart TD
    A([Request HTTP])
    A --> B["URLs — urls.py"]
    B --> C["Views / ViewSets — views.py\nSolo orquesta, no tiene logica de negocio"]
    C --> D["Services — services.py\nToda la logica de negocio vive aqui"]
    D --> E["Serializers — serializers.py\nValidacion de entrada y formato de salida"]
    E --> F["Models — models.py\nEstructura de datos y acceso a la base de datos"]
    F --> G[(PostgreSQL)]
```

### Responsabilidad de cada capa

| Capa | Archivo | Hace | No hace |
|---|---|---|---|
| URLs | `urls.py` | Enruta cada request al ViewSet correcto | Nada más |
| Views | `views.py` | Recibe el request, llama al Service, devuelve la respuesta | Lógica de negocio |
| Services | `services.py` | Genera actas, cambia estados, valida reglas de negocio | Acceso directo a HTTP |
| Serializers | `serializers.py` | Valida datos de entrada, formatea JSON de salida | Lógica de negocio |
| Models | `models.py` | Define tablas y relaciones, queries básicos | Lógica de negocio |

### Por qué Services y no lógica en las Views o los Models

Poner lógica en las Views las vuelve difíciles de testear y de reutilizar — un ViewSet está atado al ciclo HTTP. Poner lógica en los Models los convierte en clases que hacen demasiado (Fat Models). Los Services son clases o funciones Python puras, sin dependencia de HTTP ni de ORM, lo que las hace fáciles de testear unitariamente y reutilizables desde cualquier punto del sistema.

Ejemplo: cuando se confirma una entrega, el ViewSet no genera el acta ni cambia el estado de los equipos directamente. Solo llama a `AsignacionService.confirmar_entrega(asignacion_id)`, que internamente ejecuta la transacción completa.

---

## Estados de un equipo

```mermaid
stateDiagram-v2
    [*] --> DISPONIBLE
    DISPONIBLE --> EN_USO : entrega confirmada
    EN_USO --> DISPONIBLE : devolucion sin incidencias
    EN_USO --> EN_MANTENIMIENTO : incidencia LEVE
    EN_USO --> DADO_DE_BAJA : incidencia GRAVE
    EN_USO --> PERDIDO : no devuelto al cerrar acta
    EN_MANTENIMIENTO --> DISPONIBLE : ticket cerrado
    EN_MANTENIMIENTO --> DADO_DE_BAJA : irreparable
```

### Descripcion de cada estado

| Estado | Significa |
|---|---|
| DISPONIBLE | En almacen, listo para entregarse |
| EN_USO | Con un empleado actualmente |
| EN_MANTENIMIENTO | En taller, fuera de servicio temporalmente |
| DADO_DE_BAJA | Irreparable o descartado definitivamente |
| PERDIDO | Entregado a un empleado y no fue devuelto |
