from django.db import models


class StatusChoices(models.TextChoices):
    ACTIVO = "active", "Active"
    PAID = "paid", "Paid"
    OVERDUE = "overdue", "Overdue"
