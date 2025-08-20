from rest_framework import serializers

from apps.payment.models.payment import Payment
from apps.users.serializers.user_serializers import UserSerializer


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            "id",
            "code",
            "loan",
            "admin",
            "payment_date",
            "capital_amount",
            "interest_amount",
            "observation",
            "support",
            "status",
        ]
