from rest_framework import serializers
from apps.payment.models.payment import Payment


class PaymentBasicSerializer(serializers.ModelSerializer):
    date_range = serializers.SerializerMethodField()

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
            "date_range",
            "status",
        ]

    def get_date_range(self, obj):
        if obj.date_range:
            return {"start": obj.date_range.lower, "end": obj.date_range.upper}
        return None
