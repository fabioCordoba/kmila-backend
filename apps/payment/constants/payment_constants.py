from django.db import models


class StatusChoices(models.TextChoices):
    PENDING = "pending", "Pending"
    PAID = "paid", "Paid"
    OVERDUE = "overdue", "Overdue"
