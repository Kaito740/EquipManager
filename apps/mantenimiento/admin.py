from django.contrib import admin
from .models import TipoMantenimiento, TicketMantenimiento, TicketEquipo


@admin.register(TipoMantenimiento)
class TipoMantenimientoAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre']
    search_fields = ['nombre']


class TicketEquipoInline(admin.TabularInline):
    model = TicketEquipo
    extra = 0
    readonly_fields = ['equipo']


@admin.register(TicketMantenimiento)
class TicketMantenimientoAdmin(admin.ModelAdmin):
    list_display = ['id', 'tipo_mantenimiento', 'personal', 'estado', 'fecha_inicio', 'fecha_cierre']
    list_filter = ['estado', 'tipo_mantenimiento']
    search_fields = ['descripcion', 'personal__first_name', 'personal__last_name']
    # personal es readonly porque se asigna automaticamente con el usuario
    # autenticado en el Service — no debe poder falsificarse
    readonly_fields = ['fecha_inicio', 'personal']
    date_hierarchy = 'fecha_inicio'
    inlines = [TicketEquipoInline]


@admin.register(TicketEquipo)
class TicketEquipoAdmin(admin.ModelAdmin):
    list_display = ['id', 'ticket', 'equipo']
    list_filter = ['ticket__tipo_mantenimiento', 'ticket__estado']
    search_fields = ['equipo__codigo_patrimonial', 'equipo__numero_serie']
