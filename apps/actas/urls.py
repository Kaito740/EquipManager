from django.urls import path
from . import views

urlpatterns = [
    path('<int:pk>/pdf/', views.ActaPDFView.as_view(), name='acta-pdf'),
]