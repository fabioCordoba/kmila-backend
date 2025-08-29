from rest_framework import viewsets, mixins
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics


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

    permission_classes = [IsAuthenticated]
    queryset = Payment.objects.filter(is_active=True)
    serializer_class = PaymentSerializer


class PaymentSearchView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Payment.objects.all()
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
