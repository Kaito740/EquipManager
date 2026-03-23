from django.contrib import admin
from .models import Asignacion, AsignacionEquipo


class AsignacionEquipoInline(admin.TabularInline):
    model = AsignacionEquipo
    extra = 0
    readonly_fields = ['equipo']


@admin.register(Asignacion)
class AsignacionAdmin(admin.ModelAdmin):
    list_display = ['id', 'empleado', 'personal', 'sucursal', 'fecha']
    list_filter = ['sucursal', 'personal']
    search_fields = [
        'empleado__nombres',
        'empleado__apellidos',
        'empleado__dni',
        'personal__first_name',
        'personal__last_name',
    ]
    readonly_fields = ['fecha', 'sucursal']
    inlines = [AsignacionEquipoInline]
