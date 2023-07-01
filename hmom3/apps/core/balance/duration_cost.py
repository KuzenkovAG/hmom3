"""
Define function of increasing amount depend on building level:
 - Building time
 - Research time;
 - Gold amount;
 - Resources (wood, stone) amount.
"""
import math

BUILD_TIME_COEF = 0.08
SEARCH_TIME_COEF = 0.2
RES_TIME_COEF = 0.2
BUILD_EXPONENT_COEF = 3
SEARCH_EXPONENT_COEF = 2
RES_EXPONENT_COEF = 2.5
ZERO_EXPONENT = 1


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
    if level <= 10:
        a, b = (3.733, -2.33)
    elif level <= 20:
        a, b = (11.5, -80)
    else:
        a, b = (35, -550)
    result = (a * level ** 2 + b * level) * tech * res
    return int(result)


def get_resources_amount(level, tech=1, res=None):
    """Wood or stone amount depend on level."""
    if level <= 10:
        a, b = (0.066, 1.33)
    elif level <= 20:
        a, b = (0.8, -6.0)
    else:
        a, b = (2.333, -36.667)
    result = (a * level ** 2 + b * level) * tech * res
    return int(result)


if __name__ == '__main__':
    for i in range(1, 101):
        print(int(get_resources_amount(i, 1, 1)))
