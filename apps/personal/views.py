from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Cargo, Sucursal, Area, Empleado
from .serializers import CargoSerializer, SucursalSerializer, AreaSerializer, EmpleadoSerializer


class CargoListView(generics.ListAPIView):
    queryset = Cargo.objects.filter(activo=True)
    serializer_class = CargoSerializer
    permission_classes = [IsAuthenticated]


class SucursalListView(generics.ListAPIView):
    queryset = Sucursal.objects.filter(activo=True)
    serializer_class = SucursalSerializer
    permission_classes = [IsAuthenticated]


class AreaListView(generics.ListAPIView):
    queryset = Area.objects.filter(activo=True)
    serializer_class = AreaSerializer
    permission_classes = [IsAuthenticated]


class EmpleadoListView(generics.ListAPIView):
    queryset = Empleado.objects.filter(activo=True)
    serializer_class = EmpleadoSerializer
    permission_classes = [IsAuthenticated]
