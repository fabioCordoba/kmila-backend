from django.db import models
import random
import string

from django.forms import ValidationError

from apps.core.models.base_model import BaseModel
from apps.loan.constants.loan_constants import StatusChoices
from apps.users.models.user import User
from apps.wallet.constants.wallet_constants import ConceptChoices, TypeChoices
from apps.wallet.models.wallet import Wallet


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

    def clean(self):
        if not self.code:
            available = Wallet.get_available_balance()
            if not available or available < self.amount:
                raise ValidationError(
                    "No hay suficiente dinero en la caja para conceder este préstamo."
                )
            else:
                self.code = generate_code("loan")
                self.capital_balance = self.amount
                self.interest_balance = 0

    def save(self, *args, **kwargs):
        self.clean()
        # 👇 Crear movimiento en caja SOLO al crear
        if self._state.adding:
            Wallet.objects.create(
                type=TypeChoices.OUTPUT,
                concept=ConceptChoices.LOAN,
                amount=self.amount,
                observation=f"Préstamo otorgado al cliente {self.client.first_name} {self.client.last_name}, código {self.code}",
            )
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
