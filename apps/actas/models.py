from django.db import models
from django.core.exceptions import ValidationError

from apps.personal.models import Personal
from apps.equipos.models import Equipo, ChecklistItem
from apps.asignaciones.models import Asignacion
from apps.mantenimiento.models import TicketMantenimiento
from apps.utils import validar_solo_texto


class TerminosCondiciones(models.Model):

    class TipoActa(models.TextChoices):
        ENTREGA = 'ENTREGA', 'Entrega'
        DEVOLUCION = 'DEVOLUCION', 'Devolución'
        MANTENIMIENTO = 'MANTENIMIENTO', 'Mantenimiento'

    tipo_acta = models.CharField(
        max_length=20,
        choices=TipoActa.choices,
    )
    contenido = models.TextField()
    fecha_vigencia = models.DateField()
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'terminos_condiciones'
        ordering = ['tipo_acta']
        verbose_name = 'Términos y condiciones'
        verbose_name_plural = 'Términos y condiciones'

    def __str__(self):
        return f"Términos de {self.get_tipo_acta_display()} — vigente desde {self.fecha_vigencia}"

    def clean(self):
        validar_solo_texto(self.contenido, 'contenido')

    def save(self, *args, **kwargs):
        self.contenido = self.contenido.strip()
        self.full_clean()
        super().save(*args, **kwargs)


class Acta(models.Model):

    class Tipo(models.TextChoices):
        ENTREGA = 'ENTREGA', 'Entrega'
        DEVOLUCION = 'DEVOLUCION', 'Devolución'
        MANTENIMIENTO = 'MANTENIMIENTO', 'Mantenimiento'

    numero_acta = models.CharField(max_length=20, unique=True)
    tipo = models.CharField(
        max_length=20,
        choices=Tipo.choices
    )
    # asignacion_id y ticket_id son mutuamente excluyentes
    # ENTREGA y DEVOLUCION usan asignacion_id
    # MANTENIMIENTO usa ticket_id
    asignacion = models.ForeignKey(
        Asignacion,
        on_delete=models.PROTECT,
        related_name='actas',
        null=True,
        blank=True
    )
    ticket = models.ForeignKey(
        TicketMantenimiento,
        on_delete=models.PROTECT,
        related_name='actas',
        null=True,
        blank=True
    )
    personal = models.ForeignKey(
        Personal,
        on_delete=models.PROTECT,
        related_name='actas'
    )
    terminos = models.ForeignKey(
        TerminosCondiciones,
        on_delete=models.PROTECT,
        related_name='actas'
    )
    fecha = models.DateTimeField(auto_now_add=True)
    observaciones = models.TextField(blank=True, default='')

    class Meta:
        db_table = 'acta'
        ordering = ['-fecha']
        verbose_name = 'Acta'
        verbose_name_plural = 'Actas'

    def __str__(self):
        return f"Acta {self.numero_acta} — {self.get_tipo_display()}"

    def clean(self):
        # Validar que asignacion y ticket sean mutuamente excluyentes
        if self.asignacion and self.ticket:
            raise ValidationError('Un acta no puede tener asignacion y ticket al mismo tiempo.')
        if not self.asignacion and not self.ticket:
            raise ValidationError('Un acta debe tener asignacion o ticket.')

        # Validar que el tipo corresponda al campo usado
        if self.tipo in [self.Tipo.ENTREGA, self.Tipo.DEVOLUCION] and not self.asignacion:
            raise ValidationError({'tipo': 'Las actas de entrega y devolución requieren una asignación.'})
        if self.tipo == self.Tipo.MANTENIMIENTO and not self.ticket:
            raise ValidationError({'tipo': 'Las actas de mantenimiento requieren un ticket.'})

        if self.observaciones:
            validar_solo_texto(self.observaciones, 'observaciones')

    def save(self, *args, **kwargs):
        if self.observaciones:
            self.observaciones = self.observaciones.strip()
        self.numero_acta = self.numero_acta.strip()
        self.full_clean()
        super().save(*args, **kwargs)


class RespuestaChecklist(models.Model):
    acta = models.ForeignKey(
        Acta,
        on_delete=models.PROTECT,
        related_name='respuestas_checklist'
    )
    equipo = models.ForeignKey(
        Equipo,
        on_delete=models.PROTECT,
        related_name='respuestas_checklist'
    )
    checklist_item = models.ForeignKey(
        ChecklistItem,
        on_delete=models.PROTECT,
        related_name='respuestas'
    )
    respuesta = models.BooleanField()

    class Meta:
        db_table = 'respuesta_checklist'
        verbose_name = 'Respuesta de checklist'
        verbose_name_plural = 'Respuestas de checklist'
        constraints = [
            models.UniqueConstraint(
                fields=['acta', 'equipo', 'checklist_item'],
                name='unique_respuesta_checklist'
            )
        ]

    def __str__(self):
        estado = 'Conforme' if self.respuesta else 'No conforme'
        return f"{self.acta} — {self.equipo} — {self.checklist_item} — {estado}"


class Incidencia(models.Model):

    class Gravedad(models.TextChoices):
        LEVE = 'LEVE', 'Leve'
        GRAVE = 'GRAVE', 'Grave'

    equipo = models.ForeignKey(
        Equipo,
        on_delete=models.PROTECT,
        related_name='incidencias'
    )
    acta = models.ForeignKey(
        Acta,
        on_delete=models.PROTECT,
        related_name='incidencias'
    )
    descripcion = models.TextField()
    gravedad = models.CharField(
        max_length=10,
        choices=Gravedad.choices
    )
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'incidencia'
        ordering = ['-fecha']
        verbose_name = 'Incidencia'
        verbose_name_plural = 'Incidencias'

    def __str__(self):
        return f"{self.get_gravedad_display()} — {self.equipo} — {self.acta}"

    def clean(self):
        validar_solo_texto(self.descripcion, 'descripcion')

    def save(self, *args, **kwargs):
        self.descripcion = self.descripcion.strip()
        self.full_clean()
        super().save(*args, **kwargs)
