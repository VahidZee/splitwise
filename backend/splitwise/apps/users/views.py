from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.response import Response
import django.shortcuts as shortcuts
from rest_framework.decorators import action
from rest_framework import (status, viewsets, serializers as drf_serializers, permissions as drf_permissions, mixins)
from . import serializers, models, permissions
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer


class UserViewSet(
    viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
):
    """
    API for user information management and retrieval

    * **login** [`/user/login/|POST`]: obtain a valid authentication token by sending valid credentials url
    * **logout** [`/user/logout/|POST`]: invalidate currently owned authentication token
    * **retrieve** [`/user/<username>/|GET`]: obtain user information (by looking up username)
    * **update** [`/user/<ego-username>/|PUT`]: update ego user's information (excluding the password)
    * **change_password** [`/user/<ego-username>/change_password|POST`]: update user password (old password is required)
    * **friend** [`/user/friend/(<username>/)`] friend managements

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
        elif self.action in ['retrieve', 'update']:
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
        elif self.action == 'friends':
            if self.request.method == 'GET':
                return serializers.FriendSerializer
            else:
                return drf_serializers.Serializer
        return serializers.UserSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ['create', 'login']:
            permission_list = [drf_permissions.AllowAny]
        elif self.action in ['update', 'change_password', 'logout', 'friends']:
            permission_list = [permissions.IsSelfOrAdmin, drf_permissions.IsAuthenticated]
        elif self.action in ['retrieve', 'friend']:
            permission_list = [drf_permissions.IsAuthenticated]
        else:
            permission_list = [drf_permissions.AllowAny]
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
        if user.is_active:  # todo: handle account activation
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})

    @action(methods=['POST'], detail=False, )
    def logout(self, request, format=None):
        """
         Invalidate the currently owned authentication token.

         **Permissions** :

         * _Authentication_ is required
        """
        shortcuts.get_object_or_404(models.Token, user=request.user).delete()
        return Response(status=status.HTTP_202_ACCEPTED)

    @action(methods=['GET', 'POST', 'DELETE'], detail=False,
            url_path=r'(friend/(?P<username>\w*))|(friend/)',
            name='Friend', url_name='friend-api'
            )
    def friend(self, request, username=None, format=None):
        """
        APIs for retrieving and managing currently logged in user's friends.

        **Permissions**:

        - _Authentication_ is required

        **Actions & Endpoints**:

        - performing `GET` on `/user/friend/` lists all friends for the currently logged in user
        - performing `GET` on `/user/friend/<username>/` retrieves information for a specific friend of the currently
        logged in user; if no such friend was found `404 status` code will be returned
        - performing `POST` on `/user/friend/<username>/` will add the specified user to the currently logged in user's
        friend list; `201 status` code will be returned upon success
        - performing `DELETE` on `/user/friend/<username>/` will delete the specified user from the currently logged in
         user's friend list; `202 status` code will be returned upon success
        """
        if request.method == 'GET':
            if username:
                return Response(
                    serializers.FriendSerializer(shortcuts.get_object_or_404(
                        models.Friend, friend__username=username, user=request.user)).data,
                    status=status.HTTP_200_OK)
            friends = models.Friend.objects.filter(user=request.user)
            return Response(serializers.FriendSerializer(friends, many=True).data, status=status.HTTP_200_OK)
        if request.method == 'POST':
            if not username:
                return Response({'detail': 'No username was specified!'},
                                status=status.HTTP_406_NOT_ACCEPTABLE)
            friend = shortcuts.get_object_or_404(models.User, username=username)
            if request.user != friend:
                friend_obj = models.Friend(user=request.user, friend=friend)
                friend_obj.save()
                return Response(status=status.HTTP_201_CREATED)
            else:
                return Response({'detail': 'You cannot add yourself as a friend!'},
                                status=status.HTTP_406_NOT_ACCEPTABLE)
        if request.method == 'DELETE':
            if not username:
                return Response({'detail': 'No username was specified!'},
                                status=status.HTTP_406_NOT_ACCEPTABLE)
            friend_obj = shortcuts.get_object_or_404(models.Friend, friend__username=username, user=request.user)
            friend_obj.delete()
            return Response(status=status.HTTP_202_ACCEPTED)
