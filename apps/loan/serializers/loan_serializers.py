from rest_framework import serializers

from apps.loan.models.loan import Loan


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = [
            "id",
            "code",
            "client",
            "amount",
            "interest_rate",
            "capital_balance",
            "interest_balance",
            "term_months",
            "start_date",
            "status",
        ]
