from rest_framework import serializers
from apps.loan.serializers.loan_serializers import LoanSerializer
from apps.users.models import User


class LoanUserSerializer(serializers.ModelSerializer):
    loans = LoanSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "rol",
            "image",
            "is_active",
            "loans",
        ]
