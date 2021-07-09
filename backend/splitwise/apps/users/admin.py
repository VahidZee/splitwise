from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User

# website configurations
admin.site.site_header = "Donger Administration"
admin.site.site_title = "Donger"
admin.site.index_title = "Donger Management"


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'phone', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'address')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'phone', 'email', 'address', 'password1', 'password2'),
        }),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'phone', 'is_staff')


admin.site.register(User, UserAdmin)
