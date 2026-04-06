from django.urls import path
from .views import (
    TipoMantenimientoListView, 
    TicketMantenimientoListView,
    TicketMantenimientoDetailView,
    TicketMantenimientoCreateView,
    cerrar_ticket_view
)

urlpatterns = [
    path('tipos-mantenimiento/', TipoMantenimientoListView.as_view(), name='tipo-mantenimiento-list'),
    path('tickets-mantenimiento/', TicketMantenimientoListView.as_view(), name='ticket-mantenimiento-list'),
    path('tickets-mantenimiento/crear/', TicketMantenimientoCreateView.as_view(), name='ticket-mantenimiento-crear'),
    path('tickets-mantenimiento/<int:pk>/', TicketMantenimientoDetailView.as_view(), name='ticket-mantenimiento-detail'),
    path('tickets-mantenimiento/<int:pk>/cerrar/', cerrar_ticket_view, name='ticket-mantenimiento-cerrar'),
]
