from django.db import transaction
from django.utils import timezone
from apps.personal.models import Empleado
from apps.equipos.models import Equipo
from apps.asignaciones.models import Asignacion, AsignacionEquipo
from apps.actas.models import Acta, RespuestaChecklist, TerminosCondiciones
from apps.mantenimiento.models import TicketMantenimiento

def generar_numero_acta(tipo):
    letras = {'ENTREGA': 'E', 'DEVOLUCION': 'D', 'MANTENIMIENTO': 'M'}
    prefijo = letras.get(tipo)
    año = timezone.now().year

    ultimas = Acta.objects.filter(
        numero_acta__startswith=f'{prefijo}-{año}-'
    ).order_by('-numero_acta')

    if ultimas.exists():
        ultimo_num = ultimas.first().numero_acta.split('-')[-1]
        siguiente = int(ultimo_num) + 1
    else:
        siguiente = 1

    return f'{prefijo}-{año}-{siguiente:03d}'

def validar_equipos_entrega(equipo_ids):
    if not equipo_ids:
        raise ValueError('Debe incluir al menos un equipo.')

    equipos = list(Equipo.objects.filter(id__in=equipo_ids))

    if len(equipos) != len(equipo_ids):
        raise ValueError('Algunos equipos no existen.')

    for equipo in equipos:
        if equipo.estado != Equipo.Estado.DISPONIBLE:
            raise ValueError(f'El equipo {equipo.codigo_patrimonial} no está disponible.')

    return equipos

def crear_acta_entrega(personal_id, empleado_id, equipo_ids, terminos_id, observaciones='', checklist=None):
    from apps.personal.models import Personal
    
    with transaction.atomic():
        try:
            Personal.objects.get(id=personal_id)
        except Personal.DoesNotExist:
            raise ValueError(f'El personal con id {personal_id} no existe.')
        
        try:
            empleado = Empleado.objects.select_related('area__sucursal').get(id=empleado_id)
        except Empleado.DoesNotExist:
            raise ValueError(f'El empleado con id {empleado_id} no existe.')
        
        sucursal = empleado.area.sucursal

        equipos = validar_equipos_entrega(equipo_ids)

        numero_acta = generar_numero_acta('ENTREGA')

        asignacion = Asignacion.objects.create(
            empleado=empleado,
            personal_id=personal_id,
            sucursal=sucursal
        )

        for equipo in equipos:
            AsignacionEquipo.objects.create(asignacion=asignacion, equipo=equipo)

        try:
            terminos = TerminosCondiciones.objects.get(id=terminos_id)
        except TerminosCondiciones.DoesNotExist:
            raise ValueError(f'Los términos y condiciones con id {terminos_id} no existen.')

        acta = Acta.objects.create(
            numero_acta=numero_acta,
            tipo=Acta.Tipo.ENTREGA,
            asignacion=asignacion,
            personal_id=personal_id,
            terminos=terminos,
            observaciones=observaciones
        )

        if checklist:
            for item in checklist:
                RespuestaChecklist.objects.create(
                    acta=acta,
                    equipo_id=item['equipo_id'],
                    checklist_item_id=item['item_id'],
                    respuesta=item['respuesta']
                )

        Equipo.objects.filter(id__in=equipo_ids).update(estado=Equipo.Estado.EN_USO)

    return acta


def validar_checklist_mantenimiento(checklist, equipos_ticket):
    if not checklist:
        raise ValueError('El checklist es obligatorio.')

    equipos_ids_ticket = {te.equipo_id for te in equipos_ticket}

    for item in checklist:
        if item['equipo_id'] not in equipos_ids_ticket:
            raise ValueError(f'El equipo {item["equipo_id"]} no pertenece al ticket.')

    equipos_checklist = {item['equipo_id'] for item in checklist}
    if equipos_checklist != equipos_ids_ticket:
        raise ValueError('Debe completar el checklist para todos los equipos del ticket.')

    return checklist


def crear_acta_mantenimiento(personal_id, ticket_id, terminos_id, observaciones='', checklist=None):
    from apps.personal.models import Personal
    from apps.mantenimiento.models import TicketEquipo
    
    with transaction.atomic():
        try:
            Personal.objects.get(id=personal_id)
        except Personal.DoesNotExist:
            raise ValueError(f'El personal con id {personal_id} no existe.')
        
        try:
            ticket = TicketMantenimiento.objects.select_related('personal', 'tipo_mantenimiento').get(id=ticket_id)
        except TicketMantenimiento.DoesNotExist:
            raise ValueError(f'El ticket con id {ticket_id} no existe.')

        if ticket.estado != TicketMantenimiento.Estado.CERRADO:
            raise ValueError('Solo se puede crear acta de mantenimiento de tickets cerrados.')

        if Acta.objects.filter(ticket_id=ticket_id, tipo=Acta.Tipo.MANTENIMIENTO).exists():
            raise ValueError(f'Ya existe un acta de mantenimiento para el ticket {ticket_id}.')

        equipos_ticket = list(ticket.equipos.all())

        validar_checklist_mantenimiento(checklist, equipos_ticket)

        numero_acta = generar_numero_acta('MANTENIMIENTO')

        try:
            terminos = TerminosCondiciones.objects.get(id=terminos_id)
        except TerminosCondiciones.DoesNotExist:
            raise ValueError(f'Los términos y condiciones con id {terminos_id} no existen.')

        acta = Acta.objects.create(
            numero_acta=numero_acta,
            tipo=Acta.Tipo.MANTENIMIENTO,
            ticket=ticket,
            personal_id=personal_id,
            terminos=terminos,
            observaciones=observaciones
        )

        for item in checklist:
            RespuestaChecklist.objects.create(
                acta=acta,
                equipo_id=item['equipo_id'],
                checklist_item_id=item['item_id'],
                respuesta=item['respuesta']
            )

        for ticket_equipo in equipos_ticket:
            estado_anterior = ticket_equipo.estado_anterior or Equipo.Estado.DISPONIBLE
            ticket_equipo.equipo.estado = estado_anterior
            ticket_equipo.equipo.save(update_fields=['estado'])

    return acta


def validar_equipos_devolucion(asignacion_id):
    try:
        asignacion = Asignacion.objects.select_related('empleado').get(id=asignacion_id)
    except Asignacion.DoesNotExist:
        raise ValueError(f'La asignación {asignacion_id} no existe.')

    equipos = [
        ae.equipo for ae in asignacion.equipos.all()
    ]

    if not equipos:
        raise ValueError('La asignación no tiene equipos.')

    for equipo in equipos:
        if equipo.estado != Equipo.Estado.EN_USO:
            raise ValueError(f'El equipo {equipo.codigo_patrimonial} no está en uso.')

    return equipos, asignacion


def crear_acta_devolucion(personal_id, asignacion_id, terminos_id, observaciones='', checklist=None):
    from apps.personal.models import Personal
    
    with transaction.atomic():
        try:
            personal = Personal.objects.get(id=personal_id)
        except Personal.DoesNotExist:
            raise ValueError(f'El personal con id {personal_id} no existe.')
        
        equipos, asignacion = validar_equipos_devolucion(asignacion_id)

        if Acta.objects.filter(asignacion_id=asignacion_id, tipo=Acta.Tipo.DEVOLUCION).exists():
            raise ValueError(f'Ya existe un acta de devolución para la asignación {asignacion_id}.')

        numero_acta = generar_numero_acta('DEVOLUCION')

        try:
            terminos = TerminosCondiciones.objects.get(id=terminos_id)
        except TerminosCondiciones.DoesNotExist:
            raise ValueError(f'Los términos y condiciones con id {terminos_id} no existen.')

        acta = Acta.objects.create(
            numero_acta=numero_acta,
            tipo=Acta.Tipo.DEVOLUCION,
            asignacion=asignacion,
            personal_id=personal_id,
            terminos=terminos,
            observaciones=observaciones
        )

        if checklist:
            for item in checklist:
                RespuestaChecklist.objects.create(
                    acta=acta,
                    equipo_id=item['equipo_id'],
                    checklist_item_id=item['item_id'],
                    respuesta=item['respuesta']
                )

        equipos_ids = [eq.id for eq in equipos]
        Equipo.objects.filter(id__in=equipos_ids).update(estado=Equipo.Estado.DISPONIBLE)

    return acta