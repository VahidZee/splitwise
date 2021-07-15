from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from djmoney.models.fields import MoneyField
from django.utils.html import format_html


def picture_path(instance, filename):
    return f'{instance.creator.username}/{instance.pk}'


class Expense(models.Model):
    title = models.CharField(_('title'), max_length=150, blank=True, null=True,
                             help_text=_('Custom title for expense [optional].'))
    description = models.TextField(_('description'), blank=True, unique=False, null=True,
                                   help_text=_('Description of expense [optional].'))
    address = models.TextField(_('address'), blank=True, unique=False, null=True,
                               help_text=_('Location of expense [optional].'))
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False, null=False,
                                related_name='creators')

    payer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False,
                              null=False, related_name='payers')
    amount = MoneyField(max_digits=19, decimal_places=4, default_currency='USD')
    date_created = models.DateTimeField(_('date added'), auto_now_add=True)
    image = models.ImageField(upload_to=picture_path, blank=True, null=True)

    def settled(self):
        shares = Share.objects.filter(expense=self)
        return all(i.settled() for i in shares)

    def picture(self):
        return format_html(f'<img src="{self.image.url}" width="50vw">' if self.image else '')

    def shares_count(self):
        shares = Share.objects.filter(expense=self)
        return len(shares)

    def due(self):
        shares = Share.objects.filter(expense=self)
        return self.amount.amount - sum(share.share.amount for share in shares if share.settled())

    def __str__(self):
        creator = '' if self.creator == self.payer else f'({self.creator})'
        return f'{self.payer}{creator}-{self.amount}'


class Share(models.Model):
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE, blank=False, null=False,
                                related_name='shares')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False,
                             null=False, related_name='shares')
    settler = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True,
                                null=True, help_text=_('Who paid for this share (none for unpaid shares)'),
                                related_name='settles')

    share = MoneyField(_('share amount'), max_digits=19, decimal_places=4, default_currency='USD', blank=True,
                       null=True)

    def settled(self):
        return self.settler is not None

    def share_percentage(self):
        pass

    def __str__(self):
        settle = f'-({self.settler})' if self.settler else ''
        share = f'{self.share}' if self.share else ''
        return f'{share}{self.user}-{settle}'
