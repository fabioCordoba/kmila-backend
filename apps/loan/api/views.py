from rest_framework import viewsets, mixins
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated

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

    permission_classes = [IsAuthenticated]
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
