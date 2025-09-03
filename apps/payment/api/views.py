from rest_framework import viewsets, mixins
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from apps.core.permissions.permissions import IsAdminOrReadOnly, IsSuperOrReadOnly
from apps.payment.models.payment import Payment
from apps.payment.serializers.payment_serializers import PaymentSerializer


class PaymentViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """
    API endpoint to list, view, update, and delete loan.
    """

    permission_classes = [IsAuthenticated, IsSuperOrReadOnly, IsAdminOrReadOnly]
    queryset = Payment.objects.filter(is_active=True)
    serializer_class = PaymentSerializer

    def destroy(self, request, *args, **kwargs):
        payment = self.get_object()
        payment.is_active = False
        payment.save(update_fields=["is_active"])
        return Response(
            {"detail": f"El Pago {payment.code} ha sido desactivado."},
            status=status.HTTP_200_OK,
        )


class PaymentSearchView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated, IsSuperOrReadOnly, IsAdminOrReadOnly]

    def get_queryset(self):
        queryset = Payment.objects.filter(is_active=True)
        field = self.request.query_params.get("field")
        value = self.request.query_params.get("value")

        allowed_fields = [
            "code",
            "payment_date",
            "capital_amount",
            "interest_amount",
            "observation",
            "status",
            "created_at",
        ]

        if field in allowed_fields and value:
            lookup = {f"{field}__icontains": value}
            queryset = queryset.filter(**lookup)

        return queryset
