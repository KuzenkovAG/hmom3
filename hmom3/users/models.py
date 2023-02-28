from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Custom user model."""
    email = models.EmailField(
        verbose_name='Электронная почта',
        unique=True,
        error_messages={'unique': "A email already exists."},
    )
    fraction = models.ForeignKey(
        'towns.Fractions',
        on_delete=models.SET_DEFAULT,
        related_name='fractions',
        verbose_name='Фракция',
        default=1,
    )

    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
