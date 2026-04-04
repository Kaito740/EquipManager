from datetime import datetime
from django.core.exceptions import ValidationError

def validar_solo_texto(valor, campo):
    if not valor or not valor.strip():
        raise ValidationError({campo: f'El campo {campo} no puede estar vacío o contener solo espacios.'})

def validar_dni(valor):
    if valor:
        if not valor.isdigit():
            raise ValidationError({'dni': 'El DNI solo debe contener números.'})
        if len(valor) != 8:
            raise ValidationError({'dni': 'El DNI debe tener exactamente 8 dígitos.'})

def validar_equipos_para_mantenimiento(codigos_patrimoniales):
    from apps.equipos.models import Equipo
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

