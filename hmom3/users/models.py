from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Custom user model."""
    email = models.EmailField(
        'email address',
        unique=True,
        error_messages={'unique': "A email already exists."},
    )

    REQUIRED_FIELDS = []

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
