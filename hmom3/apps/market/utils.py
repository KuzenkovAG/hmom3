from django.conf import settings
from django.shortcuts import get_object_or_404

from ..towns.models import Resource

TRADE_MAP = {
    ('gold', 'wood'): 1 / settings.WOOD_PER_GOLD,
    ('gold', 'stone'): 1 / settings.STONE_PER_GOLD,
    ('wood', 'gold'): settings.GOLD_PER_WOOD,
    ('wood', 'stone'): 1 / settings.STONE_PER_WOOD,
    ('stone', 'gold'): settings.GOLD_PEF_STONE,
    ('stone', 'wood'): 1 / settings.WOOD_PER_STONE,
}


def _set_resource(resource, command, value):
    """Get resource and update it."""
    resource_amount = getattr(resource, command)
    resource_amount += value
    setattr(resource, command, resource_amount)


def trade_resources(from_r, to_r, value, user):
    """Update resources base trade course."""
    resource = get_object_or_404(Resource, user=user)
    coefficient = TRADE_MAP.get((from_r, to_r))
    _set_resource(resource, from_r + '_amount', -value)
    _set_resource(resource, to_r + '_amount', value * coefficient)
    resource.save()
