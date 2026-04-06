from django.utils import timezone
from django.db import transaction
from apps.equipos.models import Equipo
from apps.equipos.service import cambiar_componente_en_equipo
from apps.mantenimiento.models import TicketMantenimiento, TicketEquipo

def validar_equipos_para_mantenimiento(codigos_patrimoniales):
    if not codigos_patrimoniales:
        raise ValueError('Debe incluir al menos un equipo.')

    equipos = list(Equipo.objects.select_for_update().filter(codigo_patrimonial__in=codigos_patrimoniales))

    if len(equipos) != len(codigos_patrimoniales):
        raise ValueError('Algunos equipos no existen.')

    estados_invalidos = [
        Equipo.Estado.EN_MANTENIMIENTO,
        Equipo.Estado.DADO_DE_BAJA,
        Equipo.Estado.PERDIDO
    ]

    for equipo in equipos:
        if equipo.estado in estados_invalidos:
            raise ValueError(f'El equipo {equipo.codigo_patrimonial} no puede entrar a mantenimiento. Estado actual: {equipo.estado}')
    return equipos

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

def cerrar_ticket(ticket_id, personal_id, solucion='', cambios_componentes=None):
    ticket = TicketMantenimiento.objects.select_related('tipo_mantenimiento').get(id=ticket_id)

    if ticket.estado == TicketMantenimiento.Estado.CERRADO:
        raise ValueError('El ticket ya está cerrado.')

    if ticket.personal_id != personal_id:
        raise ValueError('Solo el usuario que creó el ticket puede cerrarlo.')

    if cambios_componentes is None:
        cambios_componentes = []

    now = timezone.now()
    with transaction.atomic():
        ticket.estado = TicketMantenimiento.Estado.CERRADO
        ticket.fecha_cierre = now
        ticket.solucion = solucion
        ticket.save(update_fields=['estado', 'fecha_cierre', 'solucion'])

        for ticket_equipo in ticket.equipos.all():
            ticket_equipo.equipo.estado = Equipo.Estado.DISPONIBLE
            ticket_equipo.equipo.save(update_fields=['estado'])

            for cambio in cambios_componentes:
                if cambio.get('equipo_id') == ticket_equipo.equipo_id:
                    cambiar_componente_en_equipo(
                        equipo_id=ticket_equipo.equipo_id,
                        componente_salida_id=cambio.get('componente_salida_id'),
                        componente_entrada_id=cambio.get('componente_entrada_id'),
                        fecha=now
                    )

    return ticket
