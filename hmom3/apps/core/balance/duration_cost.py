"""
Define function of increasing amount depend on building level:
 - Building time
 - Research time;
 - Gold amount;
 - Resources (wood, stone) amount.
"""

import math

from django.conf import settings


BUILD_TIME_COEF = settings.BUILD_TIME_COEF
SEARCH_TIME_COEF = settings.SEARCH_TIME_COEF
RES_TIME_COEF = settings.RES_TIME_COEF
GOLD_TIME_COEF = settings.GOLD_TIME_COEF

BUILD_EXPONENT_COEF = settings.BUILD_EXPONENT_COEF
SEARCH_EXPONENT_COEF = settings.SEARCH_EXPONENT_COEF
RES_EXPONENT_COEF = settings.RES_EXPONENT_COEF
GOLD_EXPONENT_COEF = settings.GOLD_EXPONENT_COEF

ZERO_EXPONENT = settings.ZERO_EXPONENT


def get_building_time(level, tech=1, time=None):
    """Building time depend on level."""
    result = (
        ((1 / math.e ** (level - ZERO_EXPONENT) + 1 * BUILD_TIME_COEF)
         * level ** BUILD_EXPONENT_COEF) * time / tech
    )
    return result


def get_research_time(level, tech=1, time=None):
    """Research time depend on level."""
    result = (
        ((1 / math.e ** (level - ZERO_EXPONENT) + SEARCH_TIME_COEF)
         * level ** SEARCH_EXPONENT_COEF
         ) * time / tech
    )
    return result


def get_gold_amount(level, tech=1, res=None):
    """Gold amount depend on level."""
    result = (
        (1 / math.e ** (level - ZERO_EXPONENT) + GOLD_TIME_COEF) *
        level ** GOLD_EXPONENT_COEF
    ) * res / tech
    return int(result)


def get_resources_amount(level, tech=1, res=None):
    """Wood or stone amount depend on level."""
    result = (
        (1 / math.e ** (level - ZERO_EXPONENT) + RES_TIME_COEF) *
        level ** RES_EXPONENT_COEF
    ) * res / tech
    return int(result)
