from django.contrib import admin
from .models import TerminosCondiciones, Acta, RespuestaChecklist


@admin.register(TerminosCondiciones)
class TerminosCondicionesAdmin(admin.ModelAdmin):
    list_display = ['id', 'tipo_acta', 'fecha_vigencia', 'activo']
    list_filter = ['tipo_acta', 'activo']
    search_fields = ['contenido']
    

class RespuestaChecklistInline(admin.TabularInline):
    model = RespuestaChecklist
    extra = 0
    readonly_fields = ['equipo', 'checklist_item', 'respuesta']


@admin.register(Acta)
class ActaAdmin(admin.ModelAdmin):
    list_display = ['id', 'numero_acta', 'tipo', 'personal', 'fecha']
    list_filter = ['tipo']
    search_fields = ['numero_acta', 'personal__first_name', 'personal__last_name']
    date_hierarchy = 'fecha'
    readonly_fields = ['numero_acta', 'tipo', 'asignacion', 'ticket', 'personal', 'terminos', 'fecha']
    inlines = [RespuestaChecklistInline]