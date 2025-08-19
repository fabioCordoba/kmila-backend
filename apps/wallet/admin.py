from django.contrib import admin

from apps.wallet.models.wallet import Wallet


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ["type", "concept", "amount"]
