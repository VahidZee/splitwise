from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from . import models


class ShareInline(admin.TabularInline):
    def settled(self, instance):
        return instance.settled()

    settled.boolean = True
    settled.short_description = "is settled"

    verbose_name = _('share')
    verbose_name_plural = _('shares')
    model = models.Share
    fk_name = 'expense'
    fields = ['user', 'share', 'settler', 'settled', 'updated_at']
    readonly_fields = ['settled', 'updated_at']
    autocomplete_fields = ['user', 'settler']
    extra = 0


class ExpenseAdmin(admin.ModelAdmin):

    def settled(self, instance):
        return instance.settled()

    settled.boolean = True
    settled.short_description = "is settled"

    verbose_name = _('expense')
    verbose_name_plural = _('expenses')
    model = models.Expense
    fieldsets = (
        ('Information',
         {'fields': (
             'title', 'creator', 'payer', 'date_created', 'description', 'address', 'image', 'amount')}),
    )
    autocomplete_fields = ['creator', 'payer']
    read_only_fields = ['picture']
    search_fields = ['creator__username', 'creator__phone', 'creator__email', 'creator__first_name',
                     'creator__last_name', 'payer__username', 'payer__phone', 'payer__email', 'payer__first_name',
                     'payer__last_name']
    readonly_fields = ['date_created']
    list_display = ['title', 'creator', 'payer', 'due', 'settled', 'shares_count', 'picture']
    inlines = [ShareInline]
    can_delete = True


admin.site.register(models.Expense, ExpenseAdmin)
