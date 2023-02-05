from django.db import models
from django.db.models import SlugField, CharField
from django.core.validators import RegexValidator

from .validators import SLUG_VALIDATOR, year_validator


class Category(models.Model):
    """Категории произведений."""
    name = models.CharField(
        verbose_name='Категория',
        max_length=256,
    )
    slug = models.SlugField(
        verbose_name='Адрес категории',
        max_length=50,
        unique=True,
        validators=[SLUG_VALIDATOR],
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категории'

    def __str__(self) -> SlugField:
        return self.name


class Genre(models.Model):
    """Жанры произведений."""
    name = models.CharField(
        verbose_name='Жанр',
        max_length=256,
    )
    slug = models.SlugField(
        verbose_name='Адрес жанра',
        max_length=50,
        unique=True,
        validators=[SLUG_VALIDATOR],
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Жанры'

    def __str__(self) -> CharField:
        return self.name


class Title(models.Model):
    """Произведение."""
    name = models.CharField(
        verbose_name='Название',
        max_length=256,
    )
    year = models.IntegerField(
        verbose_name='Год',
        validators=(year_validator,),
        db_index=True,
    )
    rating = models.IntegerField(
        verbose_name='Рейтинг поста',
        null=True,
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
        null=True,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория',
        blank=True,
        null=True,
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанр',
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('name',)

    def __str__(self):
        return self.name
