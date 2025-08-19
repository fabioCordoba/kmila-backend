from rest_framework import viewsets, mixins
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated


from apps.wallet.models import Wallet
from apps.wallet.serializers.wallet_serializers import WalletSerializer


class WalletViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """
    API endpoint to list, view, update, and delete wallet.
    """

    permission_classes = [IsAuthenticated]
    queryset = Wallet.objects.filter(is_active=True)
    serializer_class = WalletSerializer
