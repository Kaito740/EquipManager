from django.db import models

from apps.personal.models import Empleado, Personal, Sucursal
from apps.equipos.models import Equipo


class Asignacion(models.Model):
    empleado = models.ForeignKey(
        Empleado,
        on_delete=models.PROTECT,
        related_name='asignaciones'
    )
    personal = models.ForeignKey(
        Personal,
        on_delete=models.PROTECT,
        related_name='asignaciones'
    )
    # sucursal se jala automaticamente del area del empleado en el Service
    sucursal = models.ForeignKey(
        Sucursal,
        on_delete=models.PROTECT,
        related_name='asignaciones'
    )
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'asignacion'
        ordering = ['-fecha']
        verbose_name = 'Asignación'
        verbose_name_plural = 'Asignaciones'

    def __str__(self):
        fecha = self.fecha.strftime('%d/%m/%Y') if self.fecha else 'sin fecha'
        return f"Asignación #{self.id} — {self.empleado} — {fecha}"


class AsignacionEquipo(models.Model):
    asignacion = models.ForeignKey(
        Asignacion,
        on_delete=models.PROTECT,
        related_name='equipos'
    )
    equipo = models.ForeignKey(
        Equipo,
        on_delete=models.PROTECT,
        related_name='asignaciones'
    )

    class Meta:
        db_table = 'asignacion_equipo'
        verbose_name = 'Equipo de asignación'
        verbose_name_plural = 'Equipos de asignación'
        constraints = [
            models.UniqueConstraint(
                fields=['asignacion', 'equipo'],
                name='unique_equipo_por_asignacion'
            )
        ]

    def __str__(self):
        return f"{self.asignacion} — {self.equipo}"
