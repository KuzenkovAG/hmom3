from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from ..users import utils

User = get_user_model()


@receiver(post_save, sender=User)
def post_create_user(sender, instance, created, **kwargs):
    """Create entries in db for user."""
    if created:
        utils.set_up_user(instance)
