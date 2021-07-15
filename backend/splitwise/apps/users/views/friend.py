from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.response import Response
import django.shortcuts as shortcuts
from rest_framework import (status, viewsets, serializers as drf_serializers, permissions as drf_permissions, mixins)
from .. import serializers, models


class FriendViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.ListModelMixin,
                    mixins.DestroyModelMixin, mixins.CreateModelMixin):
    """
    APIs for retrieving and managing currently logged in user's friends.

    **Permissions**:

    - _Authentication_ is required

    **Actions & Endpoints**:

    - performing `GET` on `friend/` lists all friends for the currently logged in user
    - performing `GET` on `friend/<username>/` retrieves information for a specific friend of the currently
    logged in user; if no such friend was found `404 status` code will be returned
    - performing `POST` on `friend/<username>/` will add the specified user to the currently logged in user's
    friend list; `201 status` code will be returned upon success
    - performing `DELETE` on `friend/<username>/` will delete the specified user from the currently logged in
     user's friend list; `204 status` code will be returned upon success
    """
    queryset = models.Friend.objects.all()
    permission_classes = [drf_permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    lookup_field = 'friend__username'
    lookup_url_kwarg = 'username'
    serializer_class = serializers.FriendSerializer

    def get_serializer_class(self):
        if self.action in ['retrieve', 'list']:
            return serializers.FriendSerializer
        if self.action == 'create':
            return serializers.UsernameSerializer
        return drf_serializers.Serializer

    def filter_queryset(self, queryset):
        return queryset.filter(user=self.request.user)

    def destroy(self, request, username=None, format=None):
        if not username:
            return Response({'detail': 'No username was specified!'},
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        friend_obj = self.get_object()
        self.perform_destroy(friend_obj)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.data['username']
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
