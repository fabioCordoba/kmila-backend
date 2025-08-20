from django.db import models, transaction
from django.db.models import CASCADE, PROTECT
import random
import string

from django.forms import ValidationError

from apps.core.models.base_model import BaseModel
from apps.loan.models.loan import Loan
from apps.payment.constants.payment_constants import StatusChoices
from apps.users.models.user import User
from apps.wallet.constants.wallet_constants import ConceptChoices, TypeChoices
from apps.wallet.models.wallet import Wallet


def generate_code(name):
    initials = "".join([word[0] for word in name.split()])[:3].upper()
    numbers = "".join(random.choices(string.digits, k=3))
    return f"{initials}-{numbers}"


class Payment(BaseModel):
    code = models.CharField(max_length=255, unique=True, blank=True)
    loan = models.ForeignKey(Loan, on_delete=CASCADE, related_name="loans")
    admin = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Admin",
        related_name="payments",
        limit_choices_to={"rol": "administrator"},
    )
    payment_date = models.DateField()
    capital_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    interest_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    observation = models.TextField(blank=True, null=True)
    support = models.ImageField(
        upload_to="support/",
        null=True,
        blank=True,
    )
    status = models.CharField(
        max_length=10, choices=StatusChoices, default=StatusChoices.PENDING
    )

    def clean(self):
        if not self.code:
            # Validar que el pago no supere el saldo del préstamo
            if self.capital_amount > self.loan.capital_balance:
                raise ValidationError(
                    "El pago de capital supera la deuda pendiente de capital."
                )

            if self.interest_amount > self.loan.interest_balance:
                raise ValidationError(
                    "El pago de intereses supera la deuda pendiente de intereses."
                )

            with transaction.atomic():
                self.code = generate_code("payment")

                # --- Validar y crear movimiento de capital ---
                if self.capital_amount and self.capital_amount > 0:
                    if self.capital_amount <= self.loan.capital_balance:
                        # actualizar saldo
                        self.loan.capital_balance -= self.capital_amount
                        self.loan.save()

                        # crear movimiento en Wallet
                        Wallet.objects.create(
                            type=TypeChoices.INPUT,
                            concept=ConceptChoices.CAPITAL_PAYMENT,
                            amount=self.capital_amount,
                            observation=f"Pago de capital para préstamo {self.loan.code}",
                        )

                # --- Validar y crear movimiento de intereses ---
                if self.interest_amount and self.interest_amount > 0:
                    if self.interest_amount <= self.loan.interest_balance:
                        self.loan.interest_balance -= self.interest_amount
                        self.loan.save()

                        Wallet.objects.create(
                            type=TypeChoices.INPUT,
                            concept=ConceptChoices.INTEREST_PAYMENT,
                            amount=self.interest_amount,
                            observation=f"Pago de intereses para préstamo {self.loan.code}",
                        )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
