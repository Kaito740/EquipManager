# Decisiones técnicas — EquipManager

Registro de todas las decisiones tomadas durante el diseño, con su justificación.

| Decisión | Opción elegida | Razón |
|---|---|---|
| Base de datos | Relacional (PostgreSQL prod / SQLite dev) | Escalable, consultable, auditable |
| Atributos dinámicos | Patrón EAV | Evita JSON, permite queries complejos |
| Identificación física | Código patrimonial escrito a mano | QR eliminado — el código patrimonial ya existe en los equipos y no requiere hardware adicional |
| Arquitectura inicial | Monolito modular | Más simple para empezar, extraíble a futuro |
| Checklist | Dinámico configurable | Sin tocar código para agregar preguntas |
| Firma de conformidad | Solo técnico firma en papel | Firma de usuario paraliza el flujo si se niega |
| Notificaciones por correo | Descartado | Los flujos generan actas firmadas en papel — el correo como comprobante es redundante y agrega complejidad innecesaria |
| Campos opcionales | NULL en base de datos | Tipos correctos, integridad referencial |
| Estados y tipos | Choices en código | Son fijos por diseño del negocio |
| Permisos | Sistema nativo de Django | Reemplaza tabla Rol personalizada, más flexible y granular |
| Autenticación | JWT (djangorestframework-simplejwt) | Estándar de la industria, compatible con cualquier frontend. Access: 60 min, Refresh: 1 día |
| Consumibles | Fuera del sistema | Sin código patrimonial, no se registra |
| Código QR | Eliminado | El código patrimonial cumple la misma función de identificación sin depender de hardware adicional |
| Mantenimiento preventivo | Sin periodicidad en el sistema | Problema cultural, no técnico |
| Alertas | Solo garantías (campo fecha_garantia) | Mantenimiento preventivo descartado |
| Reportes | Solo lectura en equipos e inventario | Los reportes cubren consultas de estado y ubicación sin modificar datos |
| Inventario físico | Resuelto por los flujos | Cada movimiento queda registrado; reportes cubren el resto |
| DNI | char(8) | Identificación nacional peruana, siempre 8 dígitos |
| Descripción de mantenimiento | Texto libre | Estandarizar soluciones es inviable, cada caso es distinto |
| Sucursales | Tabla independiente con áreas | Cada sucursal tiene su propio equipo de Sistemas |
| Dirección de sucursal | Eliminada | Las sucursales mineras están en zonas remotas sin dirección postal útil — el nombre es suficiente |
| Correo de empleado | Eliminado | El sistema no envía correos — las actas se imprimen y firman físicamente |
| Términos y condiciones | Tabla propia | Permite actualizar el texto sin tocar código y tener versiones distintas por tipo de acta |
| Ticket de mantenimiento | Sin equipo_id directo | Un ticket puede incluir varios equipos — la tabla TicketEquipo resuelve la relación many-to-many |
| Número de acta | Campo propio en Acta | Identificador legible tipo 012-2025 para búsqueda rápida sin conocer el ID interno |
| Estados de equipo | DISPONIBLE, EN_USO, EN_MANTENIMIENTO, DADO_DE_BAJA, PERDIDO | ENTREGADO cambiado a EN_USO porque es más descriptivo — al leer ENTREGADO se asume que ya fue devuelto. OBSERVADO eliminado porque no tiene caso de uso real en este sistema. PERDIDO cubre equipos que no fueron devueltos |
| Borrado de equipos | Solo permitido sin historial | Un equipo sin asignaciones, tickets ni actas se puede borrar libremente. En cuanto tiene su primera asignación, PROTECT bloquea el borrado permanentemente — la única salida es marcarlo como DADO_DE_BAJA |
| Estados de ticket | Solo ABIERTO y CERRADO | EN_PROCESO no agrega valor — cuando existe el ticket ya se sabe que está en proceso, y al terminar se cierra directamente con la descripción |
| Tabla Acta unificada | Una sola tabla para los tres tipos | El número de acta es secuencial entre tipos — separar en tres tablas complicaría la generación del número. La columna ticket_id nullable no viola normalización |
| Observaciones en Acta | Texto libre con default vacío | Cubre detalles que el checklist no puede expresar con true/false. En entrega: detalles visuales preexistentes como rajaduras que no afectan funcionamiento. En devolución: contexto general del acta más allá de las incidencias. En mantenimiento: descripción de la solución aplicada |
| Testing | pytest + pytest-django | Estándar de la industria para Django |
| Variables de entorno | python-decouple | Más seguro que python-dotenv, lanza error si falta una variable |