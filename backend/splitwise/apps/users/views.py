from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.response import Response
from . import serializers
from . import models
from rest_framework.decorators import action
from rest_framework import status
from rest_framework import viewsets
from .permissions import (IsSelfOrAdmin, IsOwnerOrAdmin)
from rest_framework.permissions import AllowAny, IsAuthenticated
import rest_framework.mixins as mixins


class UserViewSet(
    viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
):
    """
    API for user information management and retrieval
    """

    lookup_field = 'username'
    lookup_url_kwarg = 'username'
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    serializer_class = serializers.EgoUserSerializer
    queryset = models.User.objects.all()

    def get_view_name(self):
        return getattr(self, 'name', 'User API') or 'User API'

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.RegistrationSerializer
        elif self.action == 'retrieve' or self.action == 'update':
            if self.request.user.is_staff or \
                    self.request.user.username == self.request.parser_context['kwargs']['username']:
                return serializers.EgoUserSerializer
            else:
                return serializers.UserSerializer
        elif self.action == 'change_password':
            return serializers.ChangePasswordSerializer
        return serializers.UserSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create':
            permission_list = [AllowAny]
        elif self.action == 'update' or self.action == 'change_password':
            permission_list = [IsOwnerOrAdmin]
        else:
            permission_list = self.permission_classes
        return [permission() for permission in permission_list]

    @action(methods=['POST'], detail=False, )
    def change_password(self, request, username=None):
        """
        Change user's passcode API.
        """
        user = request.user
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not user.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)

            # confirm the new passwords match
            new_password = serializer.data.get("new_password")
            confirm_new_password = serializer.data.get("confirm_new_password")
            if new_password != confirm_new_password:
                return Response({"new_password": ["New passwords must match"]}, status=status.HTTP_400_BAD_REQUEST)

            # set_password also hashes the password that the user will get
            user.set_password(serializer.data.get("new_password"))
            user.object.save()
            return Response({"response": "successfully changed password"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
