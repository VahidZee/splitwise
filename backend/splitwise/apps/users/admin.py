from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.models import TokenProxy
from rest_framework.authtoken.admin import TokenAdmin as DRF_TokenAdmin
from .models import User, Friend

# website configurations
admin.site.site_header = "Donger Administration"
admin.site.site_title = "Donger"
admin.site.index_title = "Donger Management"


class TokenAdmin(DRF_TokenAdmin):
    model = TokenProxy
    verbose_name = 'token'
    verbose_name_plural = 'tokens'
    autocomplete_fields = ['user']
    fields = ['user', 'key', 'created']
    readonly_fields = ['key', 'created']
    list_view = ['user__username', 'key', 'created']
    can_delete = True


class FriendsInline(admin.TabularInline):
    verbose_name = 'friend'
    verbose_name_plural = 'friends'
    model = Friend
    fk_name = 'user'
    autocomplete_fields = ['friend']
    fields = ['friend', 'date_added']
    readonly_fields = ['date_added']
    can_delete = True
    extra = 0


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
            'fields': ('username', 'phone', 'email', 'first_name', 'last_name', 'address', 'password1', 'password2'),
        }),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'phone', 'is_staff')
    inlines = [FriendsInline]


admin.site.unregister(Group)
admin.site.unregister(TokenProxy)
admin.site.register(TokenProxy, TokenAdmin)
admin.site.register(User, UserAdmin)
