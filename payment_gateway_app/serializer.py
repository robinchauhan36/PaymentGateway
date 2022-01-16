from rest_framework import serializers, exceptions
from .models import *


class CardSerializer(serializers.Serializer):
    number = serializers.CharField(max_length=16, required=True)
    expiration_month = serializers.CharField(max_length=2, required=True)
    expiration_year = serializers.CharField(max_length=4, required=True)
    cvv = serializers.CharField(max_length=3, required=True)


class PaymentDetailSerializer(serializers.ModelSerializer):
    card = CardSerializer(many=True)

    class Meta:
        model = PaymentDetail
        fields = ('amount', 'currency', 'type', 'card')
        read_only_fields = ('authorization_code', 'status')

    def create(self, validated_data):
        return PaymentDetail.objects.create(**validated_data)


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = PaymentDetail
        fields = '__all__'