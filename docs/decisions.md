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
| Notificaciones | Correo directo + tabla Notificacion | Sin Celery por ahora, se agrega si se necesita |
| Campos opcionales | NULL en base de datos | Tipos correctos, integridad referencial |
| Estados y tipos | Choices en código | Son fijos por diseño del negocio |
| Permisos | Sistema nativo de Django | Reemplaza tabla Rol personalizada, más flexible y granular |
| Autenticación | JWT (djangorestframework-simplejwt) | Estándar de la industria, compatible con cualquier frontend |
| Consumibles | Fuera del sistema | Sin código patrimonial, no se registra |
| Código QR | Eliminado | El código patrimonial cumple la misma función de identificación sin depender de hardware adicional |
| Mantenimiento preventivo | Sin periodicidad en el sistema | Problema cultural, no técnico |
| Alertas | Solo garantías (campo fecha_garantia) | Mantenimiento preventivo descartado |
| Reportes | Solo lectura en equipos e inventario | Los reportes cubren consultas de estado y ubicación sin modificar datos |
| Inventario físico | Resuelto por los flujos | Cada movimiento queda registrado; reportes cubren el resto |
| DNI | char(8) | Identificación nacional peruana, siempre 8 dígitos |
| Descripción de mantenimiento | Texto libre | Estandarizar soluciones es inviable, cada caso es distinto |
| Sucursales | Tabla independiente con áreas | Cada sucursal tiene su propio equipo de Sistemas |
| Correo | Gmail SMTP con django.core.mail | Sistema interno con pocos usuarios, sin necesidad de servicio externo |
| Testing | pytest + pytest-django | Estándar de la industria para Django |
| Variables de entorno | python-decouple | Más seguro que python-dotenv, lanza error si falta una variable |