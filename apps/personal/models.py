from django.db import models
from django.contrib.auth.models import AbstractUser
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


class Cargo(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'cargo'
        ordering = ['nombre']
        verbose_name = 'Cargo'
        verbose_name_plural = 'Cargos'

    def __str__(self):
        return self.nombre

    def clean(self):
        validar_solo_texto(self.nombre, 'nombre')

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.strip()
        self.full_clean()
        super().save(*args, **kwargs)


class Sucursal(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'sucursal'
        ordering = ['nombre']
        verbose_name = 'Sucursal'
        verbose_name_plural = 'Sucursales'

    def __str__(self):
        return self.nombre

    def clean(self):
        validar_solo_texto(self.nombre, 'nombre')

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.strip()
        self.full_clean()
        super().save(*args, **kwargs)


class Area(models.Model):
    nombre = models.CharField(max_length=100)
    sucursal = models.ForeignKey(
        Sucursal,
        on_delete=models.PROTECT,
        related_name='areas'
    )
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'area'
        ordering = ['sucursal__nombre', 'nombre']
        verbose_name = 'Área'
        verbose_name_plural = 'Áreas'
        constraints = [
            models.UniqueConstraint(
                fields=['nombre', 'sucursal'],
                name='unique_area_por_sucursal'
            )
        ]

    def __str__(self):
        return f"{self.sucursal} — {self.nombre}"

    def clean(self):
        validar_solo_texto(self.nombre, 'nombre')

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.strip()
        self.full_clean()
        super().save(*args, **kwargs)


# dni, cargo y area son nullable para permitir crear el superusuario inicial
# antes de que existan cargos y areas registrados en la base de datos.
# Una vez inicializado el sistema deben completarse desde el Django Admin.
class Personal(AbstractUser):
    dni = models.CharField(max_length=8, unique=True, null=True, blank=True)
    cargo = models.ForeignKey(
        Cargo,
        on_delete=models.PROTECT,
        related_name='personal',
        null=True,
        blank=True
    )
    area = models.ForeignKey(
        Area,
        on_delete=models.PROTECT,
        related_name='personal',
        null=True,
        blank=True
    )

    class Meta:
        db_table = 'personal'
        ordering = ['last_name', 'first_name']
        verbose_name = 'Personal'
        verbose_name_plural = 'Personal'

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"

    def clean(self):
        validar_dni(self.dni)

    def save(self, *args, **kwargs):
        if self.dni:
            self.dni = self.dni.strip()
        self.full_clean()
        super().save(*args, **kwargs)


class Empleado(models.Model):
    dni = models.CharField(max_length=8, unique=True)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    cargo = models.ForeignKey(
        Cargo,
        on_delete=models.PROTECT,
        related_name='empleados'
    )
    area = models.ForeignKey(
        Area,
        on_delete=models.PROTECT,
        related_name='empleados'
    )
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'empleado'
        ordering = ['apellidos', 'nombres']
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'

    def __str__(self):
        return f"{self.apellidos}, {self.nombres}"

    def clean(self):
        validar_dni(self.dni)
        validar_solo_texto(self.nombres, 'nombres')
        validar_solo_texto(self.apellidos, 'apellidos')

    def save(self, *args, **kwargs):
        self.dni = self.dni.strip()
        self.nombres = self.nombres.strip()
        self.apellidos = self.apellidos.strip()
        self.full_clean()
        super().save(*args, **kwargs)
