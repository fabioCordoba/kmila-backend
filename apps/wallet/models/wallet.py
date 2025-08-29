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
    observation = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["-created_at"]

    @classmethod
    def get_available_balance(cls):
        inputs = (
            cls.objects.filter(type="input").aggregate(total=models.Sum("amount"))[
                "total"
            ]
            or 0
        )
        outputs = (
            cls.objects.filter(type="output").aggregate(total=models.Sum("amount"))[
                "total"
            ]
            or 0
        )
        return inputs - outputs
