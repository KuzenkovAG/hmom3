"""
Define function of increasing resource depend on level.
"""

from django.conf import settings


DEF_GOLD_INCOME = settings.DEF_GOLD_INCOME
ROUND_COEF = 100

RESOURCE_BASE_LIMIT = {
    'gold': settings.DEF_GOLD_LIMIT,
    'wood': settings.DEF_WOOD_LIMIT,
    'stone': settings.DEF_STONE_LIMIT,
}
RESOURCE_BASE_INCOME = {
    'gold': settings.DEF_GOLD_INCOME,
    'wood': settings.DEF_WOOD_INCOME,
    'stone': settings.DEF_STONE_INCOME,
}


def get_resource_income(level, tech=1, resource=None):
    """Gold income depend on hall level and tech."""

    income = RESOURCE_BASE_INCOME.get(resource, 0)

    if level <= 10:
        a, b = (1.11, 98.99)
    elif level <= 20:
        a, b = (3, 80)
    else:
        a, b = (16, -180)
    result = (a * level ** 2 + b * level) * tech + income / 3
    return int(result)


def get_resource_limit(level, tech=1, resource=None):
    """Resources limit depend on building level and tech."""

    limit = RESOURCE_BASE_LIMIT.get(resource, 0)
    income = RESOURCE_BASE_INCOME.get(resource, 0)

    if level <= 10:
        a, b = (-1, 51)
    elif level <= 20:
        a, b = (16, -120)
    else:
        a, b = (113, -2066)
    result = (a * level ** 2 + b * level) * tech * income + limit
    return int(result) // ROUND_COEF * ROUND_COEF
