from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _


# Create your models here.
class User(AbstractUser):
    phone = PhoneNumberField(_('phone number'), blank=True, unique=True, null=True)
    address = models.TextField(_('address'), blank=True, unique=False, null=True)
