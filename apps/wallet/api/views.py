from rest_framework import viewsets, mixins
from rest_framework.views import APIView
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from django.utils.timezone import now
from datetime import date, timedelta


from apps.core.permissions.permissions import IsAdminOrReadOnly, IsSuperOrReadOnly
from apps.loan.models.loan import Loan
from apps.wallet.models import Wallet
from apps.wallet.serializers.wallet_serializers import WalletSerializer


class WalletViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """
    API endpoint to list, view, update, and delete wallet.
    """

    permission_classes = [IsAuthenticated, IsSuperOrReadOnly, IsAdminOrReadOnly]
    queryset = Wallet.objects.filter(is_active=True)
    serializer_class = WalletSerializer

    def destroy(self, request, *args, **kwargs):
        wallet = self.get_object()
        wallet.is_active = False
        wallet.save(update_fields=["is_active"])
        return Response(
            {"detail": f"El Monto {wallet.id} ha sido desactivado."},
            status=status.HTTP_200_OK,
        )


class QuickStatsView(APIView):
    """
    Endpoint that returns quick calculations for the loan business.
    """

    permission_classes = [IsAuthenticated, IsSuperOrReadOnly, IsAdminOrReadOnly]

    def get(self, request):
        today = now().date()
        first_day = today.replace(day=1)

        # calcular último día del mes
        if today.month == 12:
            last_day = date(today.year, 12, 31)
        else:
            last_day = date(today.year, today.month + 1, 1) - timedelta(days=1)

        # Calcular mes anterior
        first_day_current = today.replace(day=1)
        last_day_previous = first_day_current - timedelta(days=1)
        first_day_previous = last_day_previous.replace(day=1)

        inputs_by_month = (
            Wallet.objects.filter(
                type="input", created_at__date__range=(first_day, last_day)
            ).aggregate(total=Sum("amount"))["total"]
            or 0
        )

        outputs_by_month = (
            Wallet.objects.filter(
                type="output", created_at__date__range=(first_day, last_day)
            ).aggregate(total=Sum("amount"))["total"]
            or 0
        )

        # Sumas del mes anterior
        inputs_prev = (
            Wallet.objects.filter(
                type="input",
                created_at__date__range=(first_day_previous, last_day_previous),
            ).aggregate(total=Sum("amount"))["total"]
            or 0
        )

        outputs_prev = (
            Wallet.objects.filter(
                type="output",
                created_at__date__range=(first_day_previous, last_day_previous),
            ).aggregate(total=Sum("amount"))["total"]
            or 0
        )

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

        # Invertido en préstamos activos total
        invested_loans_total = (
            Loan.objects.filter(status="active").aggregate(total=Sum("amount"))["total"]
            or 0
        )

        # Invertido en préstamos activos actual
        invested_loans = (
            Loan.objects.filter(status="active").aggregate(
                total=Sum("capital_balance")
            )["total"]
            or 0
        )

        # Intereses pendientes
        interest_pending = (
            Loan.objects.filter(status="active").aggregate(
                total=Sum("interest_balance")
            )["total"]
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
                "inputs": inputs,
                "outputs": outputs,
                "available_capital": available_capital,
                "invested_loans_total": invested_loans_total,
                "invested_loans": invested_loans,
                "interest_earned": interest_earned,
                "interest_pending": interest_pending,
                "recovered_capital": recovered_capital,
                "inputs_by_month": inputs_by_month,
                "outputs_by_month": outputs_by_month,
                "first_day": first_day,
                "last_day": last_day,
                "inputs_prev": inputs_prev,
                "outputs_prev": outputs_prev,
                "first_day_previous": first_day_previous,
                "last_day_previous": last_day_previous,
            }
        )


class WalletSearchView(generics.ListAPIView):
    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated, IsSuperOrReadOnly, IsAdminOrReadOnly]

    def get_queryset(self):
        queryset = Wallet.objects.filter(is_active=True)
        field = self.request.query_params.get("field")
        value = self.request.query_params.get("value")

        allowed_fields = ["type", "concept", "amount", "observation", "created_at"]

        if field in allowed_fields and value:
            lookup = {f"{field}__icontains": value}
            queryset = queryset.filter(**lookup)

        return queryset
