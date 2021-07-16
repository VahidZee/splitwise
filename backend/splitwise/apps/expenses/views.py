from django.db import IntegrityError
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.response import Response
import django.shortcuts as shortcuts
from rest_framework import (status, viewsets, serializers as drf_serializers, permissions as drf_permissions, mixins,
                            decorators)
from . import serializers, models
from django.contrib.auth import get_user_model
from django.db.models import Q


class ExpenseViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.ListModelMixin,
                     mixins.DestroyModelMixin, mixins.CreateModelMixin):
    """
    APIs for retrieving and managing  users' expenses.

    **Permissions**:

    - _Authentication_ is required

    **Actions & Endpoints**:

    - performing `GET` on `/expense/` lists all expenses for the currently logged in user
    - performing `GET` on `/expense/<expense-id>/` retrieves information for a specific expense of the currently
    - performing `GET` on `/expenses/debts/[<username>/]` retrieves all the expenses of the specified user;
     if no such user was found `404 status` code will be returned. If no username is specified, debts of the currently
     logged in user will be returned
    - performing `GET` on `/expense/<expense-id>/share/[share-id/]` lists all the shares of the specified expense or
    the specified share instance
    - performing `POST` on `/expense/<expense-id>/share/` adds a newly specified share (by username) to this specific
    expense
    object; if no such user was found a `404 status` code will be returned
    - performing `POST` on `/expense/pay/<share-id>/` sets the currently logged in user as the
    settler of the specified share

    """
    queryset = models.Expense.objects.all()
    permission_classes = [drf_permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    serializer_class = serializers.ExpenseSerializer

    def get_serializer_class(self):
        if self.action in ['retrieve', 'list', 'create', 'debts']:
            return serializers.ExpenseSerializer
        if self.action in ['share']:
            return serializers.ShareSerializer
        return drf_serializers.Serializer

    def filter_queryset(self, queryset):
        if self.action == 'list':
            return queryset.filter(
                Q(creator=self.request.user) | Q(payer=self.request.user) | Q(shares__user=self.request.user) | Q(
                    shares__settler=self.request.user))
        if self.action in ['retrieve', 'share', 'debts']:
            return queryset

    def perform_create(self, serializer):
        serializer.is_valid()
        payer = serializer.validated_data['payer']
        payer = shortcuts.get_object_or_404(get_user_model(), username=payer) if payer else self.request.user
        serializer.save(creator=self.request.user, payer=payer)

    @decorators.action(methods=['POST', 'GET'], detail=True, url_path=r'(share/(?P<share_id>\w*))|(share/)')
    def share(self, request, pk=None, share_id=None, format=None):
        expense = self.get_object()
        if request.method == 'GET':
            shares = expense.shares
            if share_id:
                return Response(self.get_serializer_class()(shares.get(id=share_id)).data, status=status.HTTP_200_OK)
            return Response(self.get_serializer_class()(shares, many=True).data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        settler = shortcuts.get_object_or_404(get_user_model(), username=serializer.validated_data['settler']) if \
            serializer.validated_data['settler'] else None
        user = shortcuts.get_object_or_404(get_user_model(), username=serializer.validated_data['user'])
        share = serializer.validated_data['share']

        if request.user == expense.creator or request.user == expense.payer:
            try:
                member_obj = models.Share(expense=expense, user=user, settler=settler, share=share)
                member_obj.save()
            except IntegrityError as e:
                return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response({'detail': 'You are neither the creator or the payer of this expense, You cannot share'},
                            status=status.HTTP_406_NOT_ACCEPTABLE)

    @decorators.action(methods=['POST'], detail=False, url_path=r'(pay/(?P<share_id>\w+))')
    def pay(self, request, share_id=None, format=None):
        share = shortcuts.get_object_or_404(models.Share, id=share_id)
        if share.settled():
            return Response({'detail': f'This share is already settled by {share.settler}'},
                            status=status.HTTP_400_BAD_REQUEST)
        share.settler = request.user
        share.save()
        return Response(status=status.HTTP_202_ACCEPTED)

    @decorators.action(methods=['GET'], detail=False, url_path=r'(debts/(?P<username>\w*))|(debts/)')
    def debts(self, request, username=None, format=None):
        user = shortcuts.get_object_or_404(get_user_model(), username=username) if username else request.user
        expenses = self.get_queryset().filter(Q(shares__user=user) | Q(shares__settler=user))
        return Response(self.get_serializer_class()(expenses, many=True).data, status=status.HTTP_200_OK)
