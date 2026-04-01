from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Cargo, Sucursal, Area, Empleado
from .serializers import CargoSerializer, SucursalSerializer, AreaSerializer, EmpleadoSerializer


class CargoListView(generics.ListAPIView):
    queryset = Cargo.objects.filter(activo=True)
    serializer_class = CargoSerializer

class SucursalListView(generics.ListAPIView):
    queryset = Sucursal.objects.filter(activo=True)
    serializer_class = SucursalSerializer

class AreaListView(generics.ListAPIView):
    queryset = Area.objects.filter(activo=True)
    serializer_class = AreaSerializer

class EmpleadoListView(generics.ListAPIView):
    queryset = Empleado.objects.filter(activo=True)
    serializer_class = EmpleadoSerializer
