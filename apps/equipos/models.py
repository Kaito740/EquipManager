from django.db import models
from django.core.exceptions import ValidationError

from apps.personal.models import Sucursal
from apps.utils import validar_solo_texto


class TipoEquipo(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.CharField(max_length=255, blank=True, default='')

    class Meta:
        db_table = 'tipo_equipo'
        ordering = ['nombre']
        verbose_name = 'Tipo de equipo'
        verbose_name_plural = 'Tipos de equipo'

    def __str__(self):
        return self.nombre

    def clean(self):
        validar_solo_texto(self.nombre, 'nombre')

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.strip()
        if self.descripcion:
            self.descripcion = self.descripcion.strip()
        self.full_clean()
        super().save(*args, **kwargs)


class TipoAtributo(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'tipo_atributo'
        ordering = ['nombre']
        verbose_name = 'Tipo de atributo'
        verbose_name_plural = 'Tipos de atributo'

    def __str__(self):
        return self.nombre

    def clean(self):
        validar_solo_texto(self.nombre, 'nombre')

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.strip()
        self.full_clean()
        super().save(*args, **kwargs)


class TipoEquipoAtributo(models.Model):
    tipo_equipo = models.ForeignKey(
        TipoEquipo,
        on_delete=models.PROTECT,
        related_name='atributos'
    )
    tipo_atributo = models.ForeignKey(
        TipoAtributo,
        on_delete=models.PROTECT,
        related_name='tipos_equipo'
    )

    class Meta:
        db_table = 'tipo_equipo_atributo'
        verbose_name = 'Atributo de tipo de equipo'
        verbose_name_plural = 'Atributos de tipos de equipo'
        constraints = [
            models.UniqueConstraint(
                fields=['tipo_equipo', 'tipo_atributo'],
                name='unique_tipo_equipo_atributo'
            )
        ]

    def __str__(self):
        return f"{self.tipo_equipo} — {self.tipo_atributo}"


class Equipo(models.Model):

    class Estado(models.TextChoices):
        DISPONIBLE = 'DISPONIBLE', 'Disponible'
        EN_USO = 'EN_USO', 'En uso'
        EN_MANTENIMIENTO = 'EN_MANTENIMIENTO', 'En mantenimiento'
        DADO_DE_BAJA = 'DADO_DE_BAJA', 'Dado de baja'
        PERDIDO = 'PERDIDO', 'Perdido'

    codigo_patrimonial = models.CharField(max_length=50, unique=True)
    numero_serie = models.CharField(max_length=100, unique=True, null=True, blank=True)
    tipo_equipo = models.ForeignKey(
        TipoEquipo,
        on_delete=models.PROTECT,
        related_name='equipos'
    )
    sucursal = models.ForeignKey(
        Sucursal,
        on_delete=models.PROTECT,
        related_name='equipos'
    )
    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.DISPONIBLE
    )
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_garantia = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'equipo'
        ordering = ['codigo_patrimonial']
        verbose_name = 'Equipo'
        verbose_name_plural = 'Equipos'

    def __str__(self):
        return f"{self.codigo_patrimonial} — {self.tipo_equipo}"

    def clean(self):
        validar_solo_texto(self.codigo_patrimonial, 'codigo_patrimonial')

    def save(self, *args, **kwargs):
        self.codigo_patrimonial = self.codigo_patrimonial.strip()
        if self.numero_serie:
            self.numero_serie = self.numero_serie.strip()
        self.full_clean()
        super().save(*args, **kwargs)


class ValorAtributo(models.Model):
    equipo = models.ForeignKey(
        Equipo,
        on_delete=models.CASCADE,
        related_name='atributos'
    )
    tipo_atributo = models.ForeignKey(
        TipoAtributo,
        on_delete=models.PROTECT,
        related_name='valores'
    )
    valor = models.CharField(max_length=255)

    class Meta:
        db_table = 'valor_atributo'
        verbose_name = 'Valor de atributo'
        verbose_name_plural = 'Valores de atributo'
        constraints = [
            models.UniqueConstraint(
                fields=['equipo', 'tipo_atributo'],
                name='unique_valor_atributo_por_equipo'
            )
        ]

    def __str__(self):
        return f"{self.equipo} — {self.tipo_atributo}: {self.valor}"

    def clean(self):
        validar_solo_texto(self.valor, 'valor')

    def save(self, *args, **kwargs):
        self.valor = self.valor.strip()
        self.full_clean()
        super().save(*args, **kwargs)


class TipoComponente(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'tipo_componente'
        ordering = ['nombre']
        verbose_name = 'Tipo de componente'
        verbose_name_plural = 'Tipos de componente'

    def __str__(self):
        return self.nombre

    def clean(self):
        validar_solo_texto(self.nombre, 'nombre')

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.strip()
        self.full_clean()
        super().save(*args, **kwargs)


class Componente(models.Model):
    tipo_componente = models.ForeignKey(
        TipoComponente,
        on_delete=models.PROTECT,
        related_name='componentes'
    )
    numero_serie = models.CharField(max_length=100, unique=True, null=True, blank=True)
    descripcion = models.CharField(max_length=255)

    class Meta:
        db_table = 'componente'
        ordering = ['tipo_componente__nombre']
        verbose_name = 'Componente'
        verbose_name_plural = 'Componentes'

    def __str__(self):
        if self.numero_serie:
            return f"{self.tipo_componente} — {self.descripcion} ({self.numero_serie})"
        return f"{self.tipo_componente} — {self.descripcion}"

    def clean(self):
        validar_solo_texto(self.descripcion, 'descripcion')

    def save(self, *args, **kwargs):
        self.descripcion = self.descripcion.strip()
        if self.numero_serie:
            self.numero_serie = self.numero_serie.strip()
        self.full_clean()
        super().save(*args, **kwargs)


class EquipoComponente(models.Model):
    equipo = models.ForeignKey(
        Equipo,
        on_delete=models.CASCADE,
        related_name='componentes'
    )
    componente = models.ForeignKey(
        Componente,
        on_delete=models.PROTECT,
        related_name='equipos'
    )
    fecha_entrada = models.DateTimeField()
    # fecha_salida null significa que el componente sigue instalado en el equipo
    fecha_salida = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'equipo_componente'
        ordering = ['-fecha_entrada']
        verbose_name = 'Componente de equipo'
        verbose_name_plural = 'Componentes de equipos'

    def __str__(self):
        return f"{self.equipo} — {self.componente}"

    def clean(self):
        if self.fecha_salida and self.fecha_entrada and self.fecha_salida < self.fecha_entrada:
            raise ValidationError({'fecha_salida': 'La fecha de salida no puede ser anterior a la fecha de entrada.'})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class ChecklistItem(models.Model):
    pregunta = models.CharField(max_length=255, unique=True)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'checklist_item'
        ordering = ['pregunta']
        verbose_name = 'Ítem de checklist'
        verbose_name_plural = 'Ítems de checklist'

    def __str__(self):
        return self.pregunta

    def clean(self):
        validar_solo_texto(self.pregunta, 'pregunta')

    def save(self, *args, **kwargs):
        self.pregunta = self.pregunta.strip()
        self.full_clean()
        super().save(*args, **kwargs)


class TipoEquipoChecklist(models.Model):
    tipo_equipo = models.ForeignKey(
        TipoEquipo,
        on_delete=models.PROTECT,
        related_name='checklist_items'
    )
    checklist_item = models.ForeignKey(
        ChecklistItem,
        on_delete=models.PROTECT,
        related_name='tipos_equipo'
    )

    class Meta:
        db_table = 'tipo_equipo_checklist'
        verbose_name = 'Checklist de tipo de equipo'
        verbose_name_plural = 'Checklists de tipos de equipo'
        constraints = [
            models.UniqueConstraint(
                fields=['tipo_equipo', 'checklist_item'],
                name='unique_tipo_equipo_checklist'
            )
        ]

    def __str__(self):
        return f"{self.tipo_equipo} — {self.checklist_item}"
