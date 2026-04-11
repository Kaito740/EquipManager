from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from .models import TipoEquipo, TipoAtributo, TipoComponente, Componente, Equipo, ChecklistItem
from .serializers import (
    TipoEquipoSerializer, TipoAtributoSerializer,
    TipoComponenteSerializer, ComponenteSerializer,
    EquipoSerializer, ChecklistItemSerializer
)


class TipoEquipoListView(generics.ListAPIView):
    queryset = TipoEquipo.objects.all()
    serializer_class = TipoEquipoSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]


class TipoAtributoListView(generics.ListAPIView):
    queryset = TipoAtributo.objects.all()
    serializer_class = TipoAtributoSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]


class TipoComponenteListView(generics.ListAPIView):
    queryset = TipoComponente.objects.all()
    serializer_class = TipoComponenteSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]


class ComponenteListView(generics.ListAPIView):
    queryset = Componente.objects.all()
    serializer_class = ComponenteSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]


class EquipoListView(generics.ListAPIView):
    queryset = Equipo.objects.select_related(
        'tipo_equipo', 'sucursal'
    ).prefetch_related(
        'atributos__tipo_atributo',
        'componentes__componente__tipo_componente'
    )
    serializer_class = EquipoSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]


class EquipoDetailView(generics.RetrieveAPIView):
    queryset = Equipo.objects.select_related(
        'tipo_equipo', 'sucursal'
    ).prefetch_related(
        'atributos__tipo_atributo',
        'componentes__componente__tipo_componente'
    )
    serializer_class = EquipoSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]


class ChecklistItemListView(generics.ListAPIView):
    queryset = ChecklistItem.objects.filter(activo=True)
    serializer_class = ChecklistItemSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
