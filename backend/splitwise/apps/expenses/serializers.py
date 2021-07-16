from rest_framework import serializers
from . import models


class ShareSerializer(serializers.ModelSerializer):
    user = serializers.CharField(allow_null=False)
    settler = serializers.CharField(allow_null=True, allow_blank=True)

    class Meta:
        model = models.Share
        fields = ['id', 'user', 'settler', 'share', 'updated_at']


class ExpenseSerializer(serializers.ModelSerializer):
    creator = serializers.CharField(allow_null=False, read_only=True)
    payer = serializers.CharField(allow_null=True, allow_blank=True)
    shares = ShareSerializer(many=True, read_only=True)

    class Meta:
        model = models.Expense
        fields = '__all__'
