from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework_simplejwt.authentication import JWTAuthentication

class IsAuthenticatedForReadJWTForWrite(BasePermission):
    """
    - GET: login olmuş herkes (session veya JWT) görebilir
    - POST/PUT/DELETE: sadece JWT login izinli
    - Anonymous hiç bir şey göremez
    """
    def has_permission(self, request, view):
        # Öncelikle anonymous ise direkt reddet
        if not request.user or not request.user.is_authenticated:
            return False

        if request.method in SAFE_METHODS:
            # GET, HEAD, OPTIONS → login olmuş herkes izinli
            return True

        # POST/PUT/DELETE → sadece JWT ile giriş yapmış kullanıcı izinli
        return isinstance(getattr(request, 'successful_authenticator', None), JWTAuthentication)


class IsAuthenticatedForReadJWTEngineerWrite(IsAuthenticatedForReadJWTForWrite):
    """
    - GET: base class gibi login olmuş herkes görebilir
    - POST/PUT/DELETE: sadece JWT login + engineer grubunda izinli
    - Anonymous hiç bir şey göremez
    """
    def has_permission(self, request, view):
        # Öncelikle base sınıfın kontrolünü yap
        if not super().has_permission(request, view):
            return False

        if request.method in SAFE_METHODS:
            return True

        # POST/PUT/DELETE için engineer grubunda mı kontrol et
        is_engineer = request.user.groups.filter(name="engineer").exists()
        if not is_engineer:
            self.message = "Erişim reddedildi: Bu işlemi yapabilmek için yetkiniz bulunmuyor."
            return False
        return is_engineer and isinstance(getattr(request, 'successful_authenticator', None), JWTAuthentication)
