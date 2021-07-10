from django.contrib import admin

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from rest_framework.authtoken.models import Token
from django.contrib.auth.models import Group
from .models import User

# website configurations
admin.site.site_header = "Donger Administration"
admin.site.site_title = "Donger"
admin.site.index_title = "Donger Management"


class TokenInline(admin.StackedInline):
    model = Token
    readonly_fields = ['key', 'created']
    can_delete = False


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'phone', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'address')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions'),
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
    inlines = [TokenInline]


admin.site.unregister(Group)
admin.site.register(User, UserAdmin)
