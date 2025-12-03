from django.contrib import admin
from .models import UserType, Profile
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

@admin.register(UserType)
class UserTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'parent')
    list_filter = ('parent',)
    search_fields = ('name',)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_type', 'phone')
    search_fields = ('user__username', 'user__email')

# Profile inline form
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'

# User admin’i extend et
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)

# Re-register User admin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

