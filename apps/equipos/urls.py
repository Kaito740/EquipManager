from django.urls import path
from .views import (
    TipoEquipoListView,
    TipoAtributoListView,
    TipoComponenteListView,
    ComponenteListView,
    EquipoListView,
    EquipoDetailView,
    ChecklistItemListView
)

urlpatterns = [
    path('tipos-equipo/', TipoEquipoListView.as_view(), name='tipo-equipo-list'),
    path('tipos-atributo/', TipoAtributoListView.as_view(), name='tipo-atributo-list'),
    path('tipos-componente/', TipoComponenteListView.as_view(), name='tipo-componente-list'),
    path('componentes/', ComponenteListView.as_view(), name='componente-list'),
    path('equipos/', EquipoListView.as_view(), name='equipo-list'),
    path('equipos/<int:pk>/', EquipoDetailView.as_view(), name='equipo-detail'),
    path('checklist-items/', ChecklistItemListView.as_view(), name='checklist-item-list'),
]
