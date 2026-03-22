from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Cargo, Sucursal, Area, Personal, Empleado


@admin.register(Cargo)
class CargoAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'activo']
    list_filter = ['activo']
    search_fields = ['nombre']


@admin.register(Sucursal)
class SucursalAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'activo']
    list_filter = ['activo']
    search_fields = ['nombre']


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'sucursal', 'activo']
    list_filter = ['activo', 'sucursal']
    search_fields = ['nombre']


@admin.register(Personal)
class PersonalAdmin(UserAdmin):
    list_display = ['id', 'dni', 'username', 'first_name', 'last_name', 'email', 'cargo', 'area', 'is_active', 'is_staff']
    list_filter = ['is_active', 'is_staff', 'cargo', 'area__sucursal', 'area']
    search_fields = ['username', 'first_name', 'last_name', 'dni', 'email']
    ordering = ['last_name', 'first_name']

    fieldsets = UserAdmin.fieldsets + (
        ('Información adicional', {
            'fields': ('dni', 'cargo', 'area')
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Datos personales', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Información adicional', {
            'fields': ('dni', 'cargo', 'area')
        }),
    )


@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ['id', 'dni', 'nombres', 'apellidos', 'cargo', 'area', 'activo']
    list_filter = ['activo', 'cargo', 'area__sucursal', 'area']
    search_fields = ['nombres', 'apellidos', 'dni']
