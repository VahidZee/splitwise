from rest_framework.authentication import TokenAuthentication
from rest_framework import permissions
from rest_framework.response import Response
from . import serializers
from . import models
from rest_framework.decorators import (
    api_view, permission_classes, authentication_classes, action)
from rest_framework import status
from rest_framework import views
from rest_framework import viewsets
from rest_framework import generics
from .permissions import (IsSelfOrAdmin, IsOwnerOrAdmin)
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model


class UserViewSet(generics.GenericAPIView):
    def get_queryset(self):
        return get_user_model().objects.all()

    def get_object(self):
        pass

    @action(methods=['post'], detail=True, permission_classes=[AllowAny])
    def reset_password(self, request, forget_token):
        """
        Reset users password provided with a valid forget_token
        """
        pass

    @action(methods=['post'], detail=True, permission_classes=[AllowAny])
    def forget_password(self):
        """
        Get (by email) a forget token provided with valid user information
        """
        pass

    @action(methods=['post'], detail=True, permission_classes=[AllowAny])
    def validate_email(self):
        pass

    @action(methods=['post'], detail=True, permission_classes=[AllowAny])
    def sign_up(self):
        """
        Create
        """
        pass


class FriendViewSet(generics.ListAPIView):
    serializer_class = serializers.FriendSerializer

    def get_queryset(self):
        """
        This view should return a list of all the Friends
        for the currently authenticated user.
        """
        user = self.request.user
        return models.Friend.objects.filter(purchaser=user)


class GroupViewSet(generics.ListAPIView):
    serializer_class = serializers.GroupSerializer

    def get_queryset(self):
        """
        This view should return a list of all the Groups
        for the currently authenticated user.
        """
        user = self.request.user
        return models.Friend.objects.filter(purchaser=user)
