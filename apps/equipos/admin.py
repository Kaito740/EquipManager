from django.contrib import admin
from .models import (
    TipoEquipo, TipoAtributo, TipoEquipoAtributo,
    Equipo, ValorAtributo,
    TipoComponente, Componente, EquipoComponente,
    ChecklistItem, TipoEquipoChecklist
)


class TipoEquipoAtributoInline(admin.TabularInline):
    model = TipoEquipoAtributo
    extra = 1


class TipoEquipoChecklistInline(admin.TabularInline):
    model = TipoEquipoChecklist
    extra = 1


@admin.register(TipoEquipo)
class TipoEquipoAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'descripcion']
    search_fields = ['nombre']
    inlines = [TipoEquipoAtributoInline, TipoEquipoChecklistInline]


@admin.register(TipoAtributo)
class TipoAtributoAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre']
    search_fields = ['nombre']


@admin.register(TipoComponente)
class TipoComponenteAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre']
    search_fields = ['nombre']


class ValorAtributoInline(admin.TabularInline):
    model = ValorAtributo
    extra = 0


class EquipoComponenteInline(admin.TabularInline):
    model = EquipoComponente
    extra = 0


@admin.register(Equipo)
class EquipoAdmin(admin.ModelAdmin):
    list_display = ['id', 'codigo_patrimonial', 'numero_serie', 'tipo_equipo', 'sucursal', 'estado', 'fecha_garantia']
    list_filter = ['estado', 'tipo_equipo', 'sucursal']
    search_fields = ['codigo_patrimonial', 'numero_serie']
    readonly_fields = ['fecha_registro']
    inlines = [ValorAtributoInline, EquipoComponenteInline]


@admin.register(Componente)
class ComponenteAdmin(admin.ModelAdmin):
    list_display = ['id', 'tipo_componente', 'numero_serie', 'descripcion']
    list_filter = ['tipo_componente']
    search_fields = ['numero_serie', 'descripcion']


@admin.register(ChecklistItem)
class ChecklistItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'pregunta', 'activo']
    list_filter = ['activo']
    search_fields = ['pregunta']
