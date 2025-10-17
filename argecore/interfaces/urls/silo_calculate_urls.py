# api/urls.py
from django.urls import path
from ..viewsets.silo_calculate_views import SiloCalculationView, SiloFormAPIView

urlpatterns = [
    # Silo hesaplama endpoint'i
    path('calculate-silo/', SiloCalculationView.as_view(), name='calculate-silo'),
    path('api/silo_form/', SiloFormAPIView.as_view(), name='api_silo_form'),
]
