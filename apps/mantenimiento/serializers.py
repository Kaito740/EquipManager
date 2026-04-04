from rest_framework import serializers
from .models import TipoMantenimiento, TicketMantenimiento, TicketEquipo

class TipoMantenimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoMantenimiento
        fields = ['id', 'nombre']
        read_only_fields = ['id']

class TicketEquipoSerializer(serializers.ModelSerializer):
    equipo_codigo = serializers.CharField(source='equipo.codigo_patrimonial', read_only=True)
    equipo_estado = serializers.CharField(source='equipo.estado', read_only=True)

    class Meta:
        model = TicketEquipo
        fields = ['id', 'equipo', 'equipo_codigo', 'equipo_estado']
        read_only_fields = ['id']

class TicketMantenimientoSerializer(serializers.ModelSerializer):
    equipos = TicketEquipoSerializer(many=True, read_only=True)
    tipo_mantenimiento_nombre = serializers.CharField(source='tipo_mantenimiento.nombre', read_only=True)
    personal_nombre = serializers.CharField(source='personal.get_full_name', read_only=True)
    class Meta:
        model = TicketMantenimiento
        fields = [
            'id', 
            'personal', 
            'personal_nombre',
            'tipo_mantenimiento', 
            'tipo_mantenimiento_nombre',
            'descripcion', 
            'fecha_inicio', 
            'fecha_cierre', 
            'estado',
            'equipos'
        ]
        read_only_fields = ['id', 'fecha_inicio']

class CrearTicketMantenimientoSerializer(serializers.Serializer):
    personal = serializers.IntegerField()
    tipo_mantenimiento = serializers.IntegerField()
    descripcion = serializers.CharField()
    equipos = serializers.ListField(
        child=serializers.CharField(),
        min_length=1
    )
