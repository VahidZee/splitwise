from django.db import IntegrityError
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.response import Response
import django.shortcuts as shortcuts
from rest_framework import (status, viewsets, serializers as drf_serializers, permissions as drf_permissions, mixins,
                            decorators)
from .. import serializers, models


class CliqueViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.ListModelMixin,
                    mixins.DestroyModelMixin, mixins.CreateModelMixin):
    """
    APIs for retrieving and managing currently logged in user's cliques (a.k.a. groups).

    **Permissions**:

    - _Authentication_ is required

    **Actions & Endpoints**:

    - performing `GET` on `/clique/` lists all cliques for the currently logged in user
    - performing `GET` on `/clique/<pk>/` retrieves information for a specific clique of the currently
    logged in user; if no such clique was found `404 status` code will be returned
    - performing `POST` on `/clique/<pk>/add_member/` adds a newly specified member (by username) to this specific user
    clique; if no such user was found a `404 status` code will be returned
    - performing `DELETE` on `/clique/<pk>/remove_member/` removes the specified member (by username) from this specific
     user clique; if no such user was found a `404 status` code will be returned
    """
    queryset = models.Clique.objects.all()
    permission_classes = [drf_permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    serializer_class = serializers.CliqueSerializer

    def get_serializer_class(self):
        if self.action in ['retrieve', 'list', 'create']:
            return serializers.CliqueSerializer
        if self.action in ['add_member', 'remove_member']:
            return serializers.UsernameSerializer
        return drf_serializers.Serializer

    def filter_queryset(self, queryset):
        return queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @decorators.action(methods=['POST'], detail=True)
    def add_member(self, request, pk=None, format=None):
        clique = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.data['username']
        member = shortcuts.get_object_or_404(models.User, username=username)
        if request.user != member:
            try:
                member_obj = models.Member(clique=clique, member=member)
                member_obj.save()
            except IntegrityError:
                return Response({'detail': 'Repetitive entries were provided!'}, status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response({'detail': 'You cannot add yourself to your own group!'},
                            status=status.HTTP_406_NOT_ACCEPTABLE)

    @decorators.action(methods=['POST'], detail=True)
    def remove_member(self, request, pk=None, format=None):
        clique = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.data['username']
        member_obj = shortcuts.get_object_or_404(models.Member, clique=clique, member__username=username)
        member_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
