from django.db import models
from django.contrib.auth.models import AbstractUser

from apps.core.models.base_model import BaseModel


class User(BaseModel, AbstractUser):
    ROLES = (
        ("administrator", "Administrator"),
        ("guest", "Guest"),
    )

    email = models.EmailField(unique=True)
    rol = models.CharField(max_length=13, choices=ROLES)
    image = models.ImageField(
        upload_to="user/",
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["-created_at"]

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
