from rest_framework import serializers
from apps.loan.models.loan import Loan
from apps.loan.serializers.loan_serializers import LoanSerializer
from apps.payment.models.payment import Payment
from apps.users.models.user import User
from apps.users.serializers.user_serializers import UserSerializer
from psycopg2.extras import DateRange


class PaymentSerializer(serializers.ModelSerializer):
    loan = LoanSerializer(read_only=True)
    admin = UserSerializer(read_only=True)

    # Campos write-only para recibir IDs
    admin_id = serializers.UUIDField(write_only=True)
    loan_id = serializers.UUIDField(write_only=True)

    date_range = serializers.SerializerMethodField()
    date_range_input_start = serializers.DateField(write_only=True, required=False)
    date_range_input_end = serializers.DateField(write_only=True, required=False)

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
            "date_range",
            "date_range_input_start",  # escritura
            "date_range_input_end",
            "status",
            "admin",
            "loan",
        ]

    def create(self, validated_data):
        admin_id = validated_data.pop("admin_id")
        loan_id = validated_data.pop("loan_id")
        date_range_input_start = validated_data.pop("date_range_input_start")
        date_range_input_end = validated_data.pop("date_range_input_end")

        admin = User.objects.get(id=admin_id)
        loan = Loan.objects.get(id=loan_id)

        if date_range_input_start and date_range_input_end:
            validated_data["date_range"] = DateRange(
                date_range_input_start,
                date_range_input_end,
                bounds="[)",
            )

        return Payment.objects.create(admin=admin, loan=loan, **validated_data)

    def update(self, instance, validated_data):
        start = validated_data.pop("date_range_input_start")
        end = validated_data.pop("date_range_input_end")

        current_start = instance.date_range.lower if instance.date_range else None
        current_end = instance.date_range.upper if instance.date_range else None

        new_start = start if start else current_start
        new_end = end if end else current_end

        if new_start or new_end:
            instance.date_range = DateRange(new_start, new_end, bounds="[)")

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

    def get_date_range(self, obj):
        if obj.date_range:
            return {"start": obj.date_range.lower, "end": obj.date_range.upper}
        return None
