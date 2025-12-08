# users/urls.py
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, UserTypeViewSet, UserViewSetT, GroupViewSetT, UserTypeViewSetT

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'user-types', UserTypeViewSet, basename='user-type')
router.register("usersT", UserViewSetT, basename="usersT")
router.register("groupsT", GroupViewSetT, basename="groupsT")
router.register("user-typesT", UserTypeViewSetT, basename="user-typesT")



urlpatterns = router.urls
