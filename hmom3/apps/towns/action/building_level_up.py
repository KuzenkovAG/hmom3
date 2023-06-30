from django.shortcuts import get_object_or_404

from ...core.balance.resources import get_resource_income, get_resource_limit
from ..models import Resource


def create_hall(user, user_building, *args, **kwargs):
    """Increase gold incoming."""
    resources = get_object_or_404(Resource, user=user)
    resources.gold_income = get_resource_income(
        level=user_building.level,
        resource='gold'
    )
    resources.save()


def create_slid(user, user_building, *args, **kwargs):
    """Increase limit of storage."""
    resources = get_object_or_404(Resource, user=user)
    resources.gold_limit = get_resource_limit(
        level=user_building.level,
        resource='gold'
    )
    resources.wood_limit = get_resource_limit(
        level=user_building.level,
        resource='wood'
    )
    resources.stone_limit = resources.wood_limit
    resources.save()
