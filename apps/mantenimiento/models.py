from django.db import models
from django.core.exceptions import ValidationError

from apps.personal.models import Personal
from apps.equipos.models import Equipo
from apps.utils import validar_solo_texto


class TipoMantenimiento(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'tipo_mantenimiento'
        ordering = ['nombre']
        verbose_name = 'Tipo de mantenimiento'
        verbose_name_plural = 'Tipos de mantenimiento'

    def __str__(self):
        return self.nombre

    def clean(self):
        validar_solo_texto(self.nombre, 'nombre')

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.strip()
        self.full_clean()
        super().save(*args, **kwargs)


class TicketMantenimiento(models.Model):

    class Estado(models.TextChoices):
        ABIERTO = 'ABIERTO', 'Abierto'
        CERRADO = 'CERRADO', 'Cerrado'

    personal = models.ForeignKey(
        Personal,
        on_delete=models.PROTECT,
        related_name='tickets_mantenimiento'
    )
    tipo_mantenimiento = models.ForeignKey(
        TipoMantenimiento,
        on_delete=models.PROTECT,
        related_name='tickets'
    )
    descripcion = models.TextField()
    solucion = models.TextField(null=True, blank=True)
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    fecha_cierre = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(
        max_length=10,
        choices=Estado.choices,
        default=Estado.ABIERTO
    )

    class Meta:
        db_table = 'ticket_mantenimiento'
        ordering = ['-fecha_inicio']
        verbose_name = 'Ticket de mantenimiento'
        verbose_name_plural = 'Tickets de mantenimiento'

    def __str__(self):
        return f"Ticket #{self.id} — {self.tipo_mantenimiento} ({self.estado})"

    def clean(self):
        validar_solo_texto(self.descripcion, 'descripcion')
        if self.fecha_cierre and self.fecha_inicio and self.fecha_cierre < self.fecha_inicio:
            raise ValidationError({'fecha_cierre': 'La fecha de cierre no puede ser anterior a la fecha de inicio.'})

    def save(self, *args, **kwargs):
        self.descripcion = self.descripcion.strip()
        self.full_clean()
        super().save(*args, **kwargs)


class TicketEquipo(models.Model):
    # PROTECT porque el historial de equipos en mantenimiento es permanente
    ticket = models.ForeignKey(
        TicketMantenimiento,
        on_delete=models.PROTECT,
        related_name='equipos'
    )
    equipo = models.ForeignKey(
        Equipo,
        on_delete=models.PROTECT,
        related_name='tickets_mantenimiento'
    )

    class Meta:
        db_table = 'ticket_equipo'
        verbose_name = 'Equipo en ticket'
        verbose_name_plural = 'Equipos en tickets'
        constraints = [
            models.UniqueConstraint(
                fields=['ticket', 'equipo'],
                name='unique_ticket_equipo'
            )
        ]

    def __str__(self):
        return f"{self.ticket} — {self.equipo}"