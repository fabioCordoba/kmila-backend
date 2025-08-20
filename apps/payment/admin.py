from django.contrib import admin

from apps.payment.models.payment import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = [
        "code",
        "payment_date",
        "capital_amount",
        "interest_amount",
        "loan",
        "status",
    ]
