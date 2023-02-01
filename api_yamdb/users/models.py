from django.contrib.auth.models import AbstractUser
from django.db import models

from .enums import UserRole


class User(AbstractUser):
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        max_length=15,
        verbose_name='Роль',
        choices=UserRole.choices(),
        default=UserRole.user.name
    )
