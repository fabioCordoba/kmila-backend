from django.db import models, transaction
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

    def total_debt(self):
        """
        Returns a dictionary with the total debt broken down into principal and interest.
        """
        return {
            "capital_balance": self.capital_balance,
            "interest_balance": self.interest_balance,
            "total": self.capital_balance + self.interest_balance,
        }

    @transaction.atomic
    def apply_payment(self, payment):
        """
        Aplica un pago (Payment) al préstamo.
        - Descuenta capital e intereses.
        - Valida que no se pague más de lo debido.
        - Si ambos saldos quedan en 0, marca el préstamo como pagado.
        """

        if payment.capital_amount > self.capital_balance:
            raise ValueError("El pago de capital supera la deuda pendiente de capital.")

        if payment.interest_amount > self.interest_balance:
            raise ValueError(
                "El pago de intereses supera la deuda pendiente de intereses."
            )

        # Restar los saldos
        # self.capital_balance -= payment.capital_amount
        # self.interest_balance -= payment.interest_amount
        # --- Validar y crear movimiento de capital ---
        if payment.capital_amount and payment.capital_amount > 0:
            if payment.capital_amount <= self.capital_balance:
                # actualizar saldo
                self.capital_balance -= payment.capital_amount
                # self.loan.save()

                # crear movimiento en Wallet
                Wallet.objects.create(
                    type=TypeChoices.INPUT,
                    concept=ConceptChoices.CAPITAL_PAYMENT,
                    amount=payment.capital_amount,
                    observation=f"Pago de capital para préstamo {self.code}",
                )

        # --- Validar y crear movimiento de intereses ---
        if payment.interest_amount and payment.interest_amount > 0:
            if payment.interest_amount <= self.interest_balance:
                self.interest_balance -= payment.interest_amount
                # self.loan.save()

                Wallet.objects.create(
                    type=TypeChoices.INPUT,
                    concept=ConceptChoices.INTEREST_PAYMENT,
                    amount=payment.interest_amount,
                    observation=f"Pago de intereses para préstamo {self.code}",
                )

        # Si ya no debe nada, cambiar estado
        if self.capital_balance == 0 and self.interest_balance == 0:
            self.status = "paid"

        self.save(update_fields=["capital_balance", "interest_balance", "status"])

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
