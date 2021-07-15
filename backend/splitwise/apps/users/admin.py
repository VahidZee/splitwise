from django.contrib import admin
from django.contrib.auth.models import Group as AuthGroup
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.models import TokenProxy
from rest_framework.authtoken.admin import TokenAdmin as DRF_TokenAdmin
from . import models

# website configurations
admin.site.site_header = _("Donger Administration")
admin.site.site_title = _("Donger")
admin.site.index_title = _("Donger Management")


class TokenAdmin(DRF_TokenAdmin):
    model = TokenProxy
    verbose_name = _('Token')
    verbose_name_plural = _('Tokens')
    autocomplete_fields = ['user']
    fields = ['user', 'key', 'created']
    readonly_fields = ['key', 'created']
    list_view = ['user__username', 'key', 'created']
    can_delete = True


class FriendsInline(admin.TabularInline):
    verbose_name = _('Friend')
    verbose_name_plural = _('Friends')
    model = models.Friend
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


class MemberInline(admin.TabularInline):
    model = models.Member
    fk_name = 'clique'
    autocomplete_fields = ['member']
    search_fields = ['member__username', 'member__phone', 'member__email']
    extra = 1
    can_delete = True


class CliqueAdmin(admin.ModelAdmin):
    verbose_name = _('clique')
    verbose_name_plural = _('cliques')
    model = models.Clique
    fieldsets = (
        (None, {'fields': ('name', 'user', 'date_created')}),
    )
    autocomplete_fields = ['user']
    search_fields = ['user__username', 'user__phone', 'user__email', 'user__first_name', 'user__last_name']
    readonly_fields = ['date_created']
    list_display = ['name', 'user']
    inlines = [MemberInline]
    can_delete = True


admin.site.unregister(AuthGroup)
admin.site.unregister(TokenProxy)
admin.site.register(TokenProxy, TokenAdmin)
admin.site.register(models.User, UserAdmin)
admin.site.register(models.Clique, CliqueAdmin)
