from rest_framework import serializers
from apps.loan.models.loan import Loan
from apps.loan.serializers.loan_serializers import LoanSerializer
from apps.payment.models.payment import Payment
from apps.users.models.user import User
from apps.users.serializers.user_serializers import UserSerializer


class PaymentSerializer(serializers.ModelSerializer):
    loan = LoanSerializer(read_only=True)
    admin = UserSerializer(read_only=True)

    # Campos write-only para recibir IDs
    admin_id = serializers.UUIDField(write_only=True)
    loan_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = Payment
        fields = [
            "id",
            "code",
            "admin_id",
            "loan_id",
            "payment_date",
            "capital_amount",
            "interest_amount",
            "observation",
            "support",
            "status",
            "admin",
            "loan",
        ]

    def create(self, validated_data):
        admin_id = validated_data.pop("admin_id")
        admin = User.objects.get(id=admin_id)
        loan_id = validated_data.pop("loan_id")
        loan = Loan.objects.get(id=loan_id)
        return Payment.objects.create(admin=admin, loan=loan, **validated_data)
