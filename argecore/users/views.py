import requests
from django.shortcuts import render, redirect

# Create your views here.
# users/views.py
from rest_framework import viewsets
from rest_framework import serializers
from django.contrib.auth.models import User, Group
from .models import UserType, Profile
from .serializers import UserSerializerT, GroupSerializerT, UserTypeSerializerT, ProfilFotoSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.conf import settings
from .serializers import UserSerializer, UserTypeSerializer, EmailTokenObtainPairSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    Admin veya yetkili kullanıcılar için User + Profile yönetim viewseti
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [IsAdminUser]  # sadece admin erişebilir

class UserTypeViewSet(viewsets.ModelViewSet):
    """
    Admin veya yetkili kullanıcılar için UserType yönetim viewseti
    """
    queryset = UserType.objects.all()
    serializer_class = UserTypeSerializer
    permission_classes = [IsAdminUser]  # sadece admin erişebilir

class RegisterUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]  # herkes kayıt olabilir


class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        email = self.request.data["email"]
        # 1) Email ile kullanıcıyı bul
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise AuthenticationFailed("Kullanıcı bulunamadı.")

        if "username" not in request.data:
            # 2) Username'i ekleyelim
            request.data["username"] = user.username

        # 3) Önce JWT doğrulamasını yap
        response = super().post(request, *args, **kwargs)

        # Eğer buraya kadar geldiyse → şifre doğru, JWT üretildi
        # 4) Django session login yap
        login(request, user)

        return response
    
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Django session logout
        logout(request)
        
        # Frontend token temizleyecek, backend sadece success döner
        return Response({"detail": "Başarıyla çıkış yapıldı."}, status=status.HTTP_200_OK)
    
def password_reset_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        # Sunucunun IP veya domaini otomatik bulunur
        url = request.build_absolute_uri("/auth/users/reset_password/")

        # Djoser endpointine POST et
        response = requests.post(url, data={"email": email})

        # Djoser her zaman 204 döner → başarı
        if response.status_code == 204:
            return redirect("password_reset_done")

        messages.error(request, "Bir hata oluştu. Lütfen tekrar deneyin.")
    
    return render(request, "password_reset.html")

def password_reset_done(request):
    return render(request, "password_reset_done.html")



class UserViewSetT(viewsets.ModelViewSet):
    queryset = User.objects.all().select_related("profile")
    serializer_class = UserSerializerT
    permission_classes = [IsAdminUser] 

class GroupViewSetT(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializerT
    permission_classes = [IsAdminUser] 


class UserTypeViewSetT(viewsets.ModelViewSet):
    queryset = UserType.objects.all()
    serializer_class = UserTypeSerializerT
    permission_classes = [IsAdminUser] 

class ProfilFotoUpdateView(generics.UpdateAPIView):

    serializer_class = ProfilFotoSerializer
    permission_classes = [IsAuthenticated]

    # def permission_denied(self, request, message=None, code=None):
    #     """
    #     If request is not permitted, determine what kind of exception to raise.
    #     """
    #     if request.authenticators and not request.successful_authenticator:
    #         raise CustomAuthenticationFailed()
    #     raise exceptions.PermissionDenied(detail=message, code=code)

    def get_object(self):
        profil_nesnesi = self.request.user.profile
        return profil_nesnesi
    
    def patch(self, request, *args, **kwargs):
        response = super().patch(request, *args, **kwargs)
        return Response({
            "image": request.user.profile.image.url
        })