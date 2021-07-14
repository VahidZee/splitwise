from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.response import Response
from . import serializers
from . import models
import django.shortcuts as shortcuts
from rest_framework.decorators import action
from rest_framework import status
from rest_framework import viewsets
from rest_framework import generics
from .permissions import (IsSelfOrAdmin, IsOwnerOrAdmin)
from rest_framework.permissions import AllowAny, IsAuthenticated
import rest_framework.mixins as mixins
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.models import Token
import rest_framework.serializers as drf_serializers


class UserViewSet(
    viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
):
    """
    API for user information management and retrieval

    * **login** [`/user/login/|POST`]: obtain a valid authentication token by sending valid credentials url
    * **logout** [`/user/logout/|POST`]: invalidate currently owned authentication token
    * **retrieve** [`/user/<username>/|GET`]: obtain user information (by looking up username)
    * **update** [`/user/<ego-username>/|POST`]: update ego user's information (excluding the password)
    * **change_password** [`/user/<ego-username>/change_password|POST`]: update user password (old password is required)
    """

    lookup_field = 'username'
    lookup_url_kwarg = 'username'
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    serializer_class = serializers.EgoUserSerializer
    queryset = models.User.objects.all()

    def get_view_name(self):
        return getattr(self, 'name', 'User') or 'User'

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
        elif self.action == 'login':
            return AuthTokenSerializer
        elif self.action == 'logout':
            return drf_serializers.Serializer
        return serializers.UserSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ['create', 'login']:
            permission_list = [AllowAny]
        elif self.action in ['update', 'change_password', 'logout']:
            permission_list = [IsSelfOrAdmin, IsAuthenticated]
        elif self.action == 'retrieve':
            permission_list = [IsAuthenticated]
        else:
            permission_list = [AllowAny]
        return [permission() for permission in permission_list]

    @action(methods=['POST'], detail=False, )
    def change_password(self, request, format=None):
        """
        Change user's passcode API by providing the old password.

        **Permissions**:

        * Authentication is required
        * API only available to _Admins_ or the _Owner_ of the account
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

    @action(methods=['POST'], detail=False, )
    def login(self, request, format=None):
        """
        Obtain an authentication token by providing valid credentials.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})

    @action(methods=['POST'], detail=False, )
    def logout(self, request, format=None):
        """
         Invalidate the currently owned authentication token.

         **Permissions** :

         * _Authentication_ is required
        """
        shortcuts.get_object_or_404(Token, user=request.user).delete()
        return Response(status=status.HTTP_202_ACCEPTED)
