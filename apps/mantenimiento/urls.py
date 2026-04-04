from django.urls import path
from .views import (
    TipoMantenimientoListView, 
    TicketMantenimientoListView,
    TicketMantenimientoDetailView,
    TicketMantenimientoCreateView
)

urlpatterns = [
    path('tipos-mantenimiento/', TipoMantenimientoListView.as_view(), name='tipo-mantenimiento-list'),
    path('tickets-mantenimiento/', TicketMantenimientoListView.as_view(), name='ticket-mantenimiento-list'),
    path('tickets-mantenimiento/<int:pk>/', TicketMantenimientoDetailView.as_view(), name='ticket-mantenimiento-detail'),
    path('tickets-mantenimiento/crear/', TicketMantenimientoCreateView.as_view(), name='ticket-mantenimiento-crear'),
]
