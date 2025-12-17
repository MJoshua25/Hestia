from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'phone_number')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Security'), {'fields': ('pin_code', 'require_password_change')}),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'phone_number', 'is_staff')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'phone_number')

admin.site.register(User, CustomUserAdmin)
