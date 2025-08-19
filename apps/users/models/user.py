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
        upload_to="user/",  # 📂 se guarda en MEDIA_ROOT/portfolio/
        null=True,
        blank=True,
    )

    # USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
