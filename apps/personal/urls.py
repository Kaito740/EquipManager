from django.urls import path
from .views import (
    CargoListView,
    SucursalListView,
    AreaListView,
    EmpleadoListView
)

urlpatterns = [
    path('cargos/', CargoListView.as_view(), name='cargo-list'),
    path('sucursales/', SucursalListView.as_view(), name='sucursal-list'),
    path('areas/', AreaListView.as_view(), name='area-list'),
    path('empleados/', EmpleadoListView.as_view(), name='empleado-list'),
]
