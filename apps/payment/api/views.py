from rest_framework import viewsets, mixins
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated

from apps.loan.models.loan import Loan
from apps.loan.serializers.loan_serializers import LoanClientSerializer
from apps.payment.models.payment import Payment
from apps.payment.serializers.payment_serializers import PaymentSerializer


class PaymentViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """
    API endpoint to list, view, update, and delete loan.
    """

    permission_classes = [IsAuthenticated]
    queryset = Payment.objects.filter(is_active=True)
    serializer_class = PaymentSerializer
