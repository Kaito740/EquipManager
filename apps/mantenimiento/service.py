from django.db import transaction
from apps.mantenimiento.models import TicketMantenimiento, TicketEquipo
from apps.equipos.models import Equipo
from apps.utils import validar_equipos_para_mantenimiento

def crear_ticket(personal_id, tipo_mantenimiento_id, descripcion, codigos_patrimoniales):
    codigos_unicos = list(set(codigos_patrimoniales))
    equipos = validar_equipos_para_mantenimiento(codigos_unicos)

    with transaction.atomic():
        ticket = TicketMantenimiento.objects.create(
            personal_id=personal_id,
            tipo_mantenimiento_id=tipo_mantenimiento_id,
            descripcion=descripcion
        )

        for equipo in equipos:
            equipo.estado = Equipo.Estado.EN_MANTENIMIENTO
            equipo.save(update_fields=['estado'])
            TicketEquipo.objects.create(ticket=ticket, equipo=equipo)

    return ticket
