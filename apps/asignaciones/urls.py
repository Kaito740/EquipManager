from django.urls import path
from apps.asignaciones.views import ActaView, ActaDetailView, ActaMantenimientoView, ActaDevolucionView

urlpatterns = [
    path('actas/', ActaView.as_view(), name='actas'),
    path('actas/<int:pk>/', ActaDetailView.as_view(), name='actas-detail'),
    path('actas/mantenimiento/', ActaMantenimientoView.as_view(), name='actas-mantenimiento'),
    path('actas/devolucion/', ActaDevolucionView.as_view(), name='actas-devolucion'),
]