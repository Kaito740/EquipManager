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