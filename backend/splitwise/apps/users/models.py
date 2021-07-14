from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    phone = PhoneNumberField(
        _('phone number'), blank=True, unique=True, null=True,
        help_text=_('Personal phone number [optional].'),
    )
    address = models.TextField(
        _('address'), blank=True, unique=False, null=True,
        help_text=_('Home address [optional].'),
    )

    @property
    def user(self):
        return self


class Friend(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, related_name='friends')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False,
                               related_name='knowns')
    date_added = models.DateTimeField(_('date added'), auto_now_add=True)

    def __str__(self):
        return str(self.friend)
