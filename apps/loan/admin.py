from django.contrib import admin

from apps.loan.models.loan import Loan


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = [
        "code",
        "amount",
        "interest_rate",
        "capital_balance",
        "interest_balance",
        "status",
        "is_active",
    ]
