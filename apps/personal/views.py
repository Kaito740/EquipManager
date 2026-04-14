from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters import rest_framework as filters
from .models import Cargo, Sucursal, Area, Empleado
from .serializers import CargoSerializer, SucursalSerializer, AreaSerializer, EmpleadoSerializer


class CargoListView(generics.ListAPIView):
    queryset = Cargo.objects.filter(activo=True)
    serializer_class = CargoSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]


class SucursalListView(generics.ListAPIView):
    queryset = Sucursal.objects.filter(activo=True)
    serializer_class = SucursalSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]


class AreaListView(generics.ListAPIView):
    queryset = Area.objects.filter(activo=True)
    serializer_class = AreaSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]


class EmpleadoListView(generics.ListAPIView):
    queryset = Empleado.objects.filter(activo=True)
    serializer_class = EmpleadoSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    filter_backends = (filters.DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = ('cargo', 'area')
    search_fields = ('nombres', 'apellidos', 'dni')
    ordering_fields = ('apellidos', 'nombres', 'dni')
