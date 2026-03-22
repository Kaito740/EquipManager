# Modelo de datos — EquipManager

## Tablas y relaciones

```mermaid
erDiagram
    Cargo ||--o{ Personal : tiene
    Cargo ||--o{ Empleado : tiene
    Sucursal ||--o{ Area : tiene
    Area ||--o{ Personal : tiene
    Area ||--o{ Empleado : tiene

    Cargo {
        int id PK
        string nombre
        boolean activo
    }

    Sucursal {
        int id PK
        string nombre
        boolean activo
    }

    Area {
        int id PK
        string nombre
        int sucursal_id FK
        boolean activo
    }

    Personal {
        int id PK
        string username
        string first_name
        string last_name
        string email
        string dni
        int cargo_id FK
        int area_id FK
        boolean is_active
        boolean is_staff
    }

    Empleado {
        int id PK
        string nombre
        string apellido
        string dni
        int cargo_id FK
        int area_id FK
        boolean activo
    }

    TipoEquipo ||--o{ Equipo : clasifica
    Sucursal ||--o{ Equipo : ubicado_en
    TipoEquipo ||--o{ TipoEquipo_Atributo : tiene
    TipoAtributo ||--o{ TipoEquipo_Atributo : define
    Equipo ||--o{ ValorAtributo : tiene
    Equipo ||--o{ EquipoComponente : contiene

    TipoEquipo {
        int id PK
        string nombre
        string descripcion
    }

    TipoAtributo {
        int id PK
        string nombre
    }

    TipoEquipo_Atributo {
        int tipo_equipo_id FK
        int tipo_atributo_id FK
    }

    ValorAtributo {
        int id PK
        int equipo_id FK
        int tipo_atributo_id FK
        string valor
    }

    Equipo {
        int id PK
        string codigo_patrimonial
        string numero_serie
        int tipo_equipo_id FK
        int sucursal_id FK
        string estado
        datetime fecha_registro
        date fecha_garantia
    }

    TipoComponente ||--o{ Componente : tipifica
    Componente ||--o{ EquipoComponente : esta_en

    TipoComponente {
        int id PK
        string nombre
    }

    Componente {
        int id PK
        int tipo_componente_id FK
        string numero_serie
        string descripcion
    }

    EquipoComponente {
        int id PK
        int equipo_id FK
        int componente_id FK
        datetime fecha_entrada
        datetime fecha_salida
    }

    TipoEquipo ||--o{ TipoEquipo_Checklist : requiere
    ChecklistItem ||--o{ TipoEquipo_Checklist : integra
    ChecklistItem ||--o{ RespuestaChecklist : evalua
    Acta ||--o{ RespuestaChecklist : registra

    ChecklistItem {
        int id PK
        string pregunta
        boolean activo
    }

    TipoEquipo_Checklist {
        int tipo_equipo_id FK
        int checklist_item_id FK
    }

    Empleado ||--o{ Asignacion : recibe
    Personal ||--o{ Asignacion : registra
    Sucursal ||--o{ Asignacion : ubicada_en
    Asignacion ||--o{ AsignacionEquipo : incluye
    Equipo ||--o{ AsignacionEquipo : asignado

    Asignacion {
        int id PK
        int empleado_id FK
        int personal_id FK
        int sucursal_id FK
        datetime fecha
    }

    AsignacionEquipo {
        int id PK
        int asignacion_id FK
        int equipo_id FK
    }

    TipoMantenimiento ||--o{ TicketMantenimiento : tipifica
    Personal ||--o{ TicketMantenimiento : ejecuta
    TicketMantenimiento ||--o{ TicketEquipo : incluye
    Equipo ||--o{ TicketEquipo : intervenido_en

    TipoMantenimiento {
        int id PK
        string nombre
    }

    TicketMantenimiento {
        int id PK
        int personal_id FK
        int tipo_mantenimiento_id FK
        text descripcion
        datetime fecha_inicio
        datetime fecha_cierre
        string estado
    }

    TicketEquipo {
        int id PK
        int ticket_id FK
        int equipo_id FK
    }

    TerminosCondiciones ||--o{ Acta : aplica_en
    Asignacion ||--o{ Acta : genera
    TicketMantenimiento ||--o{ Acta : genera
    Personal ||--o{ Acta : firma
    Acta ||--o{ Incidencia : registra
    Acta ||--o{ RespuestaChecklist : contiene
    Equipo ||--o{ RespuestaChecklist : evaluado_en

    TerminosCondiciones {
        int id PK
        string tipo_acta
        text contenido
        date fecha_vigencia
        boolean activo
    }

    Acta {
        int id PK
        string numero_acta
        string tipo
        int asignacion_id FK
        int ticket_id FK
        int personal_id FK
        int terminos_id FK
        datetime fecha
        text observaciones
    }

    RespuestaChecklist {
        int id PK
        int acta_id FK
        int equipo_id FK
        int checklist_item_id FK
        boolean respuesta
    }

    Incidencia {
        int id PK
        int equipo_id FK
        int acta_id FK
        text descripcion
        string gravedad
        datetime fecha
    }
```

## Apps y sus modelos

### personal
`Cargo`, `Sucursal`, `Area`, `Personal` (AbstractUser), `Empleado`

### equipos
`TipoEquipo`, `TipoAtributo`, `TipoEquipo_Atributo`, `ValorAtributo`, `Equipo`, `TipoComponente`, `Componente`, `EquipoComponente`, `ChecklistItem`, `TipoEquipo_Checklist`

### asignaciones
`Asignacion`, `AsignacionEquipo`

### mantenimiento
`TipoMantenimiento`, `TicketMantenimiento`, `TicketEquipo`

**Choices de `TicketMantenimiento.estado`:** `ABIERTO`, `CERRADO`

**Choices de `Equipo.estado`:** `DISPONIBLE`, `ENTREGADO`, `EN_MANTENIMIENTO`, `OBSERVADO`, `DADO_DE_BAJA`, `PERDIDO`

**Choices de `Acta.tipo`:** `ENTREGA`, `DEVOLUCION`, `MANTENIMIENTO`

**Choices de `Incidencia.gravedad`:** `LEVE`, `GRAVE`

**Choices de `TerminosCondiciones.tipo_acta`:** `ENTREGA`, `DEVOLUCION`, `MANTENIMIENTO`

**Nota sobre `Acta`:** Una sola tabla cubre los tres tipos. `asignacion_id` y `ticket_id` son mutuamente excluyentes — uno siempre es null. El tipo `DEVOLUCION` referencia la misma `asignacion_id` que la `ENTREGA` original, lo que permite comparar el estado del equipo entre ambos momentos.

**Uso de `observaciones` por tipo de acta:**
- `ENTREGA` — detalles visuales preexistentes que el checklist no puede capturar con true/false. Ejemplo: *"Laptop con rajadura en puerto USB derecho, preexistente al momento de la entrega"*
- `DEVOLUCION` — contexto general del acta más allá de las incidencias por equipo. Ejemplo: *"Devolución por fin de contrato, pendiente trámite de mouse perdido"*
- `MANTENIMIENTO` — descripción de la solución aplicada. Ejemplo: *"Se reemplazó disco duro por SSD 512GB, instalación limpia de Windows 11 Pro"*

### actas
`TerminosCondiciones`, `Acta`, `RespuestaChecklist`, `Incidencia`
