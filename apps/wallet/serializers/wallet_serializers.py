from rest_framework import serializers

from apps.wallet.models.wallet import Wallet


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = [
            "id",
            "type",
            "concept",
            "amount",
            "observation",
            "created_at",
            "updated_at",
        ]
