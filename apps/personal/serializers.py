from rest_framework import serializers
from .models import Cargo, Sucursal, Area, Empleado


class CargoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cargo
        fields = ['id', 'nombre']
        read_only_fields = ['id']

    def validate_nombre(self, value):
        return value.strip()


class SucursalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sucursal
        fields = ['id', 'nombre']
        read_only_fields = ['id']

    def validate_nombre(self, value):
        return value.strip()


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ['id', 'nombre', 'sucursal']
        read_only_fields = ['id']

    def validate_nombre(self, value):
        return value.strip()


class EmpleadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empleado
        fields = ['id', 'dni', 'nombres', 'apellidos', 'cargo', 'area']
        read_only_fields = ['id']