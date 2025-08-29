from rest_framework import serializers
from apps.payment.models.payment import Payment


class PaymentBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            "id",
            "code",
            "payment_date",
            "capital_amount",
            "interest_amount",
            "observation",
            "support",
            "status",
        ]
