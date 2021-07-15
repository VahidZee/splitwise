from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


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

    @property
    def name(self):
        return f'{self.first_name} {self.last_name}'


class Friend(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, related_name='friends')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False,
                               related_name='knowns')
    date_added = models.DateTimeField(_('date added'), auto_now_add=True)

    class Meta:
        unique_together = ('user', 'friend',)

    def clean(self):
        if self.user == self.friend:
            raise ValidationError(_('Users cannot be friends with themselves.'))

    def __str__(self):
        return str(self.friend)


class Clique(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, related_name='cliques')
    name = models.CharField(
        _('name'),
        max_length=150, unique=False, blank=True, null=True,
        help_text=_('What to name the group [optional].'),
    )
    date_created = models.DateTimeField(_('date created'), auto_now_add=True)

    def count_members(self):
        return self.members.count()

    class Meta:
        unique_together = ('user', 'name',)

    def __str__(self):
        return f'{self.user}{"-" + str(self.name) if self.name else ""}'


class Member(models.Model):
    clique = models.ForeignKey(Clique, on_delete=models.CASCADE, null=False, blank=False, related_name='members')
    member = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, related_name='participants')

    def clean(self):
        if self.clique.user == self.member:
            raise ValidationError(_('Users cannot be a member of their own cliques.'))

    class Meta:
        unique_together = ('clique', 'member',)
