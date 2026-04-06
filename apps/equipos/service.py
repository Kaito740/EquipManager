from django.utils import timezone
from django.db import transaction
from apps.equipos.models import EquipoComponente, Componente


def agregar_componente_a_equipo(equipo_id, componente_id, fecha=None):
    componente = Componente.objects.get(id=componente_id)
    
    if EquipoComponente.objects.filter(
        componente_id=componente_id,
        fecha_salida__isnull=True
    ).exists():
        raise ValueError('El componente ya está instalado en otro equipo.')
    
    with transaction.atomic():
        equipocomponente = EquipoComponente.objects.create(
            equipo_id=equipo_id,
            componente=componente,
            fecha_entrada=fecha or timezone.now()
        )
    
    return equipocomponente


def retirar_componente_de_equipo(equipo_id, componente_id, fecha=None):
    equipocomponente = EquipoComponente.objects.select_related('componente', 'equipo').get(
        equipo_id=equipo_id,
        componente_id=componente_id,
        fecha_salida__isnull=True
    )
    
    with transaction.atomic():
        equipocomponente.fecha_salida = fecha or timezone.now()
        equipocomponente.save(update_fields=['fecha_salida'])
    
    return equipocomponente


def cambiar_componente_en_equipo(equipo_id, componente_salida_id, componente_entrada_id, fecha=None):
    with transaction.atomic():
        if componente_salida_id:
            retirar_componente_de_equipo(equipo_id, componente_salida_id, fecha)
        
        if componente_entrada_id:
            agregar_componente_a_equipo(equipo_id, componente_entrada_id, fecha)
    
    return True
