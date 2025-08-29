from rest_framework import serializers

from apps.loan.models.loan import Loan
from apps.payment.serializers.payment_basic_serializers import PaymentBasicSerializer
from apps.users.models.user import User
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
    user_id = serializers.UUIDField(write_only=True)
    client = UserSerializer(read_only=True)
    user_payments = PaymentBasicSerializer(many=True, read_only=True)
    total_interest_amount = serializers.DecimalField(
        max_digits=12, decimal_places=2, read_only=True
    )
    total_amount_to_pay = serializers.DecimalField(
        max_digits=12, decimal_places=2, read_only=True
    )
    accrued_interest = serializers.DecimalField(
        max_digits=12, decimal_places=2, read_only=True
    )
    days_elapsed = serializers.DecimalField(
        max_digits=12, decimal_places=2, read_only=True
    )
    # paid_payment_dates = serializers.ListField(
    #     child=serializers.DateField(format="%Y-%m-%d"), read_only=True
    # )

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
            "updated_at",
            "total_interest_amount",
            "total_amount_to_pay",
            "accrued_interest",
            "days_elapsed",
            "status",
            "client",
            "user_payments",
            "user_id",
            # "paid_payment_dates",
        ]

    def create(self, validated_data):
        user_id = validated_data.pop("user_id")
        user = User.objects.get(id=user_id)
        return Loan.objects.create(client=user, **validated_data)
