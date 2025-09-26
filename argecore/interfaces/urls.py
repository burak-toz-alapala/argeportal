from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets.silo_calculate_views import SiloCalculationView, MaterialViewSet, MaterialComboboxViewSet
from .viewsets.silo_calculate_views import PressureFillDataView, PressureDischargeDataView, PressureFillHopperDataView, PressureDischargeHopperDataView, PressureFillAndDischargeHopperDataView
from .views import *

router = DefaultRouter()
router.register(r'materials', MaterialViewSet, basename="materials")
router.register(r'cb_materials', MaterialComboboxViewSet, basename="cb_materials")
urlpatterns = [
    # Silo hesaplama endpoint'i
    path('api/calculate-silo/', SiloCalculationView.as_view(), name='calculate-silo'),
    path("api/fill-pressures/", PressureFillDataView.as_view(), name="pressure-data-fill"),
    path("api/disc-pressures/", PressureDischargeDataView.as_view(), name="pressure-data-discharge"),
    path("api/fill-hopper/", PressureFillHopperDataView.as_view(), name="pressure-data-fill-hopper"),
    path("api/disc-hopper/", PressureDischargeHopperDataView.as_view(), name="pressure-data-discharge-hopper"),
    path("api/fill--disc-hopper/", PressureFillAndDischargeHopperDataView.as_view(), name="pressure-data-fill-discharge-hopper"),
    path('api/', include(router.urls)),
    path('', home_page, name='home'),
    path('tmp', tmp_page, name='tmp'),
]
