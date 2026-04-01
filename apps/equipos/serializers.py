from rest_framework import serializers
from .models import TipoEquipo, TipoAtributo, TipoComponente, Componente, Equipo, ChecklistItem, ValorAtributo, EquipoComponente


class TipoAtributoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoAtributo
        fields = ['id', 'nombre']
        read_only_fields = ['id']

class TipoComponenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoComponente
        fields = ['id', 'nombre']
        read_only_fields = ['id']

class ComponenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Componente
        fields = ['id', 'tipo_componente', 'numero_serie', 'descripcion']
        read_only_fields = ['id']
        depth = 1

class ValorAtributoSerializer(serializers.ModelSerializer):
    tipo_atributo = TipoAtributoSerializer(read_only=True)
    class Meta:
        model = ValorAtributo
        fields = ['id', 'tipo_atributo', 'valor']
        read_only_fields = ['id']

class EquipoComponenteSerializer(serializers.ModelSerializer):
    componente = ComponenteSerializer(read_only=True)
    class Meta:
        model = EquipoComponente
        fields = ['id', 'componente', 'fecha_entrada', 'fecha_salida']
        read_only_fields = ['id']

class TipoEquipoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoEquipo
        fields = ['id', 'nombre', 'descripcion']
        read_only_fields = ['id']

class EquipoSerializer(serializers.ModelSerializer):
    atributos = ValorAtributoSerializer(many=True, read_only=True)
    componentes = EquipoComponenteSerializer(many=True, read_only=True)
    class Meta:
        model = Equipo
        fields = ['id', 'codigo_patrimonial', 'numero_serie', 'tipo_equipo', 'sucursal', 'estado', 'fecha_registro', 'fecha_garantia', 'atributos', 'componentes']
        read_only_fields = ['id', 'fecha_registro']
        depth = 1

class ChecklistItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChecklistItem
        fields = ['id', 'pregunta']
        read_only_fields = ['id']
