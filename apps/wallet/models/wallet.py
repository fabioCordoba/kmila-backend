from django.db import models

from apps.core.models.base_model import BaseModel
from apps.wallet.constants.wallet_constants import ConceptChoices, TypeChoices


class Wallet(BaseModel):
    type = models.CharField(
        max_length=20, choices=TypeChoices.choices, default=TypeChoices.INPUT
    )
    concept = models.CharField(
        max_length=20, choices=ConceptChoices.choices, default=ConceptChoices.OTHER
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    # loan = models.ForeignKey(
    #     "Loan",
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     blank=True,
    #     related_name="transactions",
    # )
    observation = models.TextField(blank=True, null=True)
