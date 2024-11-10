# payments/serializers.py
from rest_framework import serializers

from app.models.payment import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
class PaymentZalo(serializers.Serializer):
    payment = serializers.IntegerField(required=True)
