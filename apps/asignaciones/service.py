from django.db import transaction
from django.utils import timezone
from apps.personal.models import Empleado
from apps.equipos.models import Equipo
from apps.asignaciones.models import Asignacion, AsignacionEquipo
from apps.actas.models import Acta, RespuestaChecklist, TerminosCondiciones

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
    with transaction.atomic():
        empleado = Empleado.objects.select_related('area__sucursal').get(id=empleado_id)
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

        terminos = TerminosCondiciones.objects.get(id=terminos_id)

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