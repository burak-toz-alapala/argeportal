from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets.silo_calculate_views import SiloCalculationView, MaterialViewSet, MaterialComboboxViewSet
from .viewsets.silo_calculate_views import PressureDataView
from .views import *

router = DefaultRouter()
router.register(r'materials', MaterialViewSet, basename="materials")
router.register(r'cb_materials', MaterialComboboxViewSet, basename="cb_materials")
urlpatterns = [
    # Silo hesaplama endpoint'i
    path('api/calculate-silo/', SiloCalculationView.as_view(), name='calculate-silo'),
    path("api/fill-pressures/", PressureDataView.as_view(), name="pressure-data"),
    path('api/', include(router.urls)),
    path('', home_page, name='home'),
]
