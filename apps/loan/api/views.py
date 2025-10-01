from rest_framework import viewsets, mixins
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from apps.core.permissions.permissions import IsAdminOrReadOnly, IsSuperOrReadOnly
from apps.loan.models.loan import Loan
from apps.loan.serializers.loan_serializers import LoanClientSerializer


class LoanViewSet(
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
    queryset = Loan.objects.filter(is_active=True)
    serializer_class = LoanClientSerializer

    def destroy(self, request, *args, **kwargs):
        loan = self.get_object()
        loan.is_active = False
        loan.save(update_fields=["is_active"])
        return Response(
            {"detail": f"El Prestamo {loan.code} ha sido desactivado."},
            status=status.HTTP_200_OK,
        )


class LoanSearchView(generics.ListAPIView):
    serializer_class = LoanClientSerializer
    permission_classes = [IsAuthenticated, IsSuperOrReadOnly, IsAdminOrReadOnly]

    def get_queryset(self):
        queryset = Loan.objects.filter(is_active=True)
        field = self.request.query_params.get("field")
        value = self.request.query_params.get("value")

        allowed_fields = [
            "code",
            "amount",
            "interest_rate",
            "term_months",
            "start_date",
            "status",
            "created_at",
            "day",
            "month",
            "year",
        ]

        if field in allowed_fields and value:
            if field == "day":
                queryset = queryset.filter(start_date__day=value)
            elif field == "month":
                queryset = queryset.filter(start_date__month=value)
            elif field == "year":
                queryset = queryset.filter(start_date__year=value)
            else:
                lookup = {f"{field}__icontains": value}
                queryset = queryset.filter(**lookup)

        return queryset
