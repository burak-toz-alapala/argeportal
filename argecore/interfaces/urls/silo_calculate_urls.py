# api/urls.py
from django.urls import path
from ..viewsets.silo_calculate_views import SiloCalculationView

urlpatterns = [
    # Silo hesaplama endpoint'i
    path('calculate-silo/', SiloCalculationView.as_view(), name='calculate-silo'),
]
