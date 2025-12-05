"""
URL configuration for argecore project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.urls import reverse_lazy
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from users.views import EmailTokenObtainPairView, LogoutView, password_reset_view, password_reset_done

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('interfaces.urls')),
    path('user/', include('users.urls')),

    path('auth/', include(('djoser.urls', 'djoser'), namespace='djoser')),
    path("auth/", include("djoser.urls.jwt")),
    path('api-auth/', include('rest_framework.urls')),
    path('auth/jwt/create/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/jwt/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', EmailTokenObtainPairView.as_view(), name="email_token_obtain_pair"),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('refresh/', TokenRefreshView.as_view(), name="token_refresh"),
    path('password/reset/complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name="password_reset_complete.html"
         ),
         name='password_reset_complete'),
    path("password/reset/confirm/<uidb64>/<token>/",
         auth_views.PasswordResetConfirmView.as_view(
             template_name="password_reset_confirm.html"
         ),
         name="password_reset_confirm"),
    path('password/change/',
         auth_views.PasswordChangeView.as_view(
             success_url=reverse_lazy('auth_password_change_done'),
             template_name="registration/password_change_form.html"),
         name='auth_password_change'),
    path('password/change/done/',
         auth_views.PasswordChangeDoneView.as_view(),
         name='auth_password_change_done'),
    path("password/reset/", password_reset_view, name="password_reset_form"),
    path("password/reset/done/", password_reset_done, name="password_reset_done"),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG == True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL)