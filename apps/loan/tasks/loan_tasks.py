from celery import shared_task
from django.utils import timezone

from apps.loan.models.loan import Loan


@shared_task
def accrue_interest():
    today = timezone.now().date()
    loans = Loan.objects.filter(status="active")

    for loan in loans:
        # Calcular interés mensual simple (puedes ajustar fórmula)
        monthly_interest = (loan.amount * loan.interest_rate) / 100

        loan.interest_balance += monthly_interest
        loan.save(update_fields=["interest_balance"])
