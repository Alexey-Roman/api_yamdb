from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from .enums import UserRole


class User(AbstractUser):
    username = models.CharField(
        max_length=150,
        verbose_name='Логин',
        unique=True,
        db_index=True,
        validators=[RegexValidator(
            regex=r'^[\w.@+-]+\Z',
            message='В логине разрешены только буквы, цифры и символы  @.+-_'
        )]
    )
    email = models.EmailField(
        max_length=254,
        verbose_name='email',
        unique=True
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя',
        blank=True
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия',
        blank=True
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
    )
    role = models.CharField(
        max_length=15,
        verbose_name='Роль',
        choices=UserRole.choices(),
        default=UserRole.user.name
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)

    def __str__(self):
        return self.username
