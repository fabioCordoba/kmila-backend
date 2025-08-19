from django.db import models
import random
import string

from apps.core.models.base_model import BaseModel
from apps.loan.constants.loan_constants import StatusChoices
from apps.users.models.user import User


def generate_code(name):
    initials = "".join([word[0] for word in name.split()])[:3].upper()
    numbers = "".join(random.choices(string.digits, k=3))
    return f"{initials}-{numbers}"


class Loan(BaseModel):
    code = models.CharField(max_length=255, unique=True, blank=True)
    client = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Client",
        related_name="loans",
        limit_choices_to={"rol": "guest"},
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)

    capital_balance = models.DecimalField(
        max_digits=12, decimal_places=2, blank=True, null=True
    )
    interest_balance = models.DecimalField(
        max_digits=12, decimal_places=2, blank=True, null=True
    )
    term_months = models.IntegerField()
    start_date = models.DateField()
    status = models.CharField(
        max_length=10, choices=StatusChoices, default=StatusChoices.ACTIVO
    )

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = generate_code("loan")
            self.capital_balance = self.amount
            self.interest_balance = 0
        super().save(*args, **kwargs)

    @property
    def total_interest_amount(self):
        """Calculate the total interest payable on the entire loan (simple, not compound)."""
        return (self.amount * self.interest_rate * self.term_months) / 100

    @property
    def total_amount_to_pay(self):
        """Capital + interest."""
        return self.amount + self.total_interest_amount

    @property
    def monthly_payment(self):
        """Fixed monthly payment (principal + simple interest)."""
        return self.total_amount_to_pay / self.term_months

    def __str__(self):
        return f"Loan {self.code} - {self.client.email}"
