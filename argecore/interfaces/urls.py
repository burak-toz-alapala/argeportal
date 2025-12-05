from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets.silo_calculate_views import SiloCalculationView, MaterialViewSet, MaterialComboboxViewSet, SiloFormAPIView
from .viewsets.silo_calculate_views import PressureFillDataView, PressureDischargeDataView, PressureFillHopperDataView, PressureDischargeHopperDataView, PressureFillAndDischargeHopperDataView
from .viewsets.mail_sender_views import MailSenderT
from .views import *

router = DefaultRouter()
router.register(r'materials', MaterialViewSet, basename="materials")
router.register(r'cb_materials', MaterialComboboxViewSet, basename="cb_materials")
urlpatterns = [
    # Silo hesaplama endpoint'i
    path('api/calculate-silo/', SiloCalculationView.as_view(), name='calculate-silo'),
    path('api/silo_form/', SiloFormAPIView.as_view(), name='api_silo_form'),
    path("api/fill-pressures/", PressureFillDataView.as_view(), name="pressure-data-fill"),
    path("api/disc-pressures/", PressureDischargeDataView.as_view(), name="pressure-data-discharge"),
    path("api/fill-hopper/", PressureFillHopperDataView.as_view(), name="pressure-data-fill-hopper"),
    path("api/disc-hopper/", PressureDischargeHopperDataView.as_view(), name="pressure-data-discharge-hopper"),
    path("api/fill--disc-hopper/", PressureFillAndDischargeHopperDataView.as_view(), name="pressure-data-fill-discharge-hopper"),
    path('api/', include(router.urls)),
    path('', home_page, name='home'),
    path('tmp', tmp_page, name='tmp'),
    path('login', login_page, name='login'),
    path('no-permissions', no_permissions_page, name='no-permissions'),
    path('profile', profile_page, name='profile'),
    path('mail_sender', MailSenderT.as_view(), name='mail_sender'),
]
