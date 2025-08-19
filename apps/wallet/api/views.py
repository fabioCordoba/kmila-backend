from rest_framework import viewsets, mixins
from rest_framework.views import APIView
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum
from rest_framework.response import Response


from apps.loan.models.loan import Loan
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


class QuickStatsView(APIView):
    """
    Endpoint that returns quick calculations for the loan business.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        # input and output
        inputs = (
            Wallet.objects.filter(type="input").aggregate(total=Sum("amount"))["total"]
            or 0
        )
        outputs = (
            Wallet.objects.filter(type="output").aggregate(total=Sum("amount"))["total"]
            or 0
        )
        available_capital = inputs - outputs

        # Invertido en préstamos activos
        invested_loans = (
            Loan.objects.filter(status="active").aggregate(total=Sum("amount"))["total"]
            or 0
        )

        # Intereses ganados
        interest_earned = (
            Wallet.objects.filter(type="input", concept="interest_payment").aggregate(
                total=Sum("amount")
            )["total"]
            or 0
        )

        # Capital recuperado
        recovered_capital = (
            Wallet.objects.filter(type="input", concept="capital_payment").aggregate(
                total=Sum("amount")
            )["total"]
            or 0
        )

        return Response(
            {
                "available_capital": available_capital,
                "invested_loans": invested_loans,
                "interest_earned": interest_earned,
                "recovered_capital": recovered_capital,
            }
        )
