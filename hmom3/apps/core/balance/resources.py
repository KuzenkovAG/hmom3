"""
Define function of increasing user resource depend on level.
"""
from django.conf import settings

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
    result = (a * level ** 2 + b * level) * tech / 3 + income / 2
    return int(result)


def get_resource_limit(level, tech=1, resource=None):
    """Resources limit depend on building level and tech."""

    limit = RESOURCE_BASE_LIMIT.get(resource, 0)

    if level == 0:
        return limit
    elif level <= 10:
        a, b = (0.3889, 1.1111)
    elif level <= 20:
        a, b = (2, -15)
    else:
        a, b = (14.167, -258.333)
    result = (a * level ** 2 + b * level) * tech * limit

    # округляем результат до 100х единиц
    if limit > ROUND_COEF:
        return int(result) // ROUND_COEF * ROUND_COEF
    return int(result)


if __name__ == '__main__':
    resource = 'gold'
    for i in range(1, 101):
        print(get_resource_income(i, 1, resource))
