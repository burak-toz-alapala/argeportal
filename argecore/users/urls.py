# users/urls.py
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, UserTypeViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'user-types', UserTypeViewSet, basename='user-type')


urlpatterns = router.urls
