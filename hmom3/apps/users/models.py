from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user model."""
    email = models.EmailField(
        verbose_name='Электронная почта',
        unique=True,
        error_messages={'unique': "A email already exists."},
    )
    fraction = models.ForeignKey(
        'towns.Fraction',
        on_delete=models.SET_NULL,
        related_name='user_fraction',
        verbose_name='Фракция',
        default=1,
        null=True,
    )

    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
