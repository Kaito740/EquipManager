from rest_framework import serializers
from apps.actas.models import Acta, RespuestaChecklist


class ActaListSerializer(serializers.ModelSerializer):
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    empleado_nombre = serializers.CharField(source='asignacion.empleado.nombres', read_only=True)
    empleado_apellido = serializers.CharField(source='asignacion.empleado.apellidos', read_only=True)

    class Meta:
        model = Acta
        fields = ['id', 'numero_acta', 'tipo', 'tipo_display', 'fecha', 'empleado_nombre', 'empleado_apellido']
        read_only_fields = ['id']

class RespuestaChecklistSerializer(serializers.ModelSerializer):
    equipo_codigo = serializers.CharField(source='equipo.codigo_patrimonial', read_only=True)
    pregunta = serializers.CharField(source='checklist_item.pregunta', read_only=True)

    class Meta:
        model = RespuestaChecklist
        fields = ['equipo_codigo', 'pregunta', 'respuesta']


class ActaDetailSerializer(serializers.ModelSerializer):
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    empleado_nombre = serializers.CharField(source='asignacion.empleado.nombres', read_only=True)
    empleado_apellido = serializers.CharField(source='asignacion.empleado.apellidos', read_only=True)
    checklist = RespuestaChecklistSerializer(source='respuestas_checklist', many=True, read_only=True)

    class Meta:
        model = Acta
        fields = [
            'id', 'numero_acta', 'tipo', 'tipo_display', 'fecha',
            'empleado_nombre', 'empleado_apellido', 'observaciones', 'checklist'
        ] 

class ActaCreateSerializer(serializers.Serializer):
    empleado_id = serializers.IntegerField()
    equipos = serializers.ListField(child=serializers.IntegerField(), min_length=1)
    terminos_id = serializers.IntegerField()
    observaciones = serializers.CharField(required=False, allow_blank=True, default='')
    checklist = serializers.ListField(required=False, default=list)

    def validate_equipos(self, value):
        if len(value) != len(set(value)):
            raise serializers.ValidationError('No puede haber equipos duplicados.')
        return value