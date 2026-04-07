from django.urls import path
from apps.asignaciones.views import ActaView, ActaDetailView

urlpatterns = [
    path('actas/', ActaView.as_view(), name='actas'),
    path('actas/<int:pk>/', ActaDetailView.as_view(), name='actas-detail'),
]