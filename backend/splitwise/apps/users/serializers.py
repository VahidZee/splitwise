from abc import ABC

from rest_framework import serializers
from .models import User
from django.utils.translation import gettext_lazy as _


class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'confirm_password', 'address', 'first_name', 'last_name']
        extra_kwargs = {
            'password': {'write_only': True, 'style': {'input_type': 'password'}},
        }

    def save(self):
        user = User(
            username=self.validated_data['username'],
            email=self.validated_data['email'],
            address=self.validated_data['address'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
        )
        confirm, password = self.validated_data['confirm_password'], self.validated_data['password']
        if confirm and password and confirm == password:
            user.set_password(password)
            user.save()
            user.is_active = False  # wait until email activation
        else:
            raise serializers.ValidationError({'password_mismatch': _('The two password fields didn’t match.')})
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']
        read_only_fields = fields


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True, style={'input_type': 'password'})
    new_password = serializers.CharField(required=True, write_only=True, style={'input_type': 'password'})
    confirm_new_password = serializers.CharField(required=True, write_only=True, style={'input_type': 'password'})


class EgoUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'address', 'phone']

