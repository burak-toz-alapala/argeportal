from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile, UserType


# ----- Profile Inline -----
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "Profil Bilgileri"
    extra = 1   # Yeni kullanıcı eklerken 1 profil formu göster


# ----- User Admin -----
class UserAdmin(BaseUserAdmin):
    
    # Yeni kullanıcı eklerken görülecek alanlar
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username',
                'first_name',
                'last_name',
                'email',
                'password1',
                'password2',
                'groups',        # Gruplar burada!
                'is_active',
                'is_staff',
            ),
        }),
    )

    inlines = [ProfileInline]

    def get_inline_instances(self, request, obj=None):
        """
        Yeni kullanıcı oluştururken de inline profil formu gösterilsin.
        """
        return [inline(self.model, self.admin_site) for inline in self.inlines]


# Default admin’i unregister edip yenisini ekliyoruz
admin.site.unregister(User)
admin.site.register(User, UserAdmin)



# ----- UserType admin -----
@admin.register(UserType)
class UserTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'parent')
    search_fields = ('name',)


# ----- Profile admin -----
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_type', 'phone')
    search_fields = ('user__username', 'user__email')
