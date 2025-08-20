from rest_framework import serializers

from apps.loan.models.loan import Loan
from apps.payment.serializers.payment_serializers import PaymentBasicSerializer
from apps.users.serializers.user_serializers import UserSerializer


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = [
            "id",
            "code",
            "amount",
            "interest_rate",
            "capital_balance",
            "interest_balance",
            "term_months",
            "start_date",
            "status",
        ]


class LoanClientSerializer(serializers.ModelSerializer):
    client = UserSerializer(read_only=True)
    user_payments = PaymentBasicSerializer(many=True, read_only=True)

    class Meta:
        model = Loan
        fields = [
            "id",
            "code",
            "amount",
            "interest_rate",
            "capital_balance",
            "interest_balance",
            "term_months",
            "start_date",
            "status",
            "client",
            "user_payments",
        ]
