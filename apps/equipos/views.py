from rest_framework import generics
from .models import TipoEquipo, TipoAtributo, TipoComponente, Componente, Equipo, ChecklistItem
from .serializers import (
    TipoEquipoSerializer, TipoAtributoSerializer,
    TipoComponenteSerializer, ComponenteSerializer,
    EquipoSerializer, ChecklistItemSerializer
)


class TipoEquipoListView(generics.ListAPIView):
    queryset = TipoEquipo.objects.all()
    serializer_class = TipoEquipoSerializer


class TipoAtributoListView(generics.ListAPIView):
    queryset = TipoAtributo.objects.all()
    serializer_class = TipoAtributoSerializer


class TipoComponenteListView(generics.ListAPIView):
    queryset = TipoComponente.objects.all()
    serializer_class = TipoComponenteSerializer


class ComponenteListView(generics.ListAPIView):
    queryset = Componente.objects.all()
    serializer_class = ComponenteSerializer


class EquipoListView(generics.ListAPIView):
    queryset = Equipo.objects.select_related(
        'tipo_equipo', 'sucursal'
    ).prefetch_related(
        'atributos__tipo_atributo',
        'componentes__componente__tipo_componente'
    )
    serializer_class = EquipoSerializer


class EquipoDetailView(generics.RetrieveAPIView):
    queryset = Equipo.objects.select_related(
        'tipo_equipo', 'sucursal'
    ).prefetch_related(
        'atributos__tipo_atributo',
        'componentes__componente__tipo_componente'
    )
    serializer_class = EquipoSerializer


class ChecklistItemListView(generics.ListAPIView):
    queryset = ChecklistItem.objects.filter(activo=True)
    serializer_class = ChecklistItemSerializer
