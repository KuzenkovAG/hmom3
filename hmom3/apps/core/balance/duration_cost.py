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
        a, b = (127.7, -77)
    elif level <= 20:
        a, b = (630, -5100)
    else:
        a, b = (4250, -77500)
    result = (a * level ** 2 + b * level) * tech + res / 3
    return int(result)


def get_resources_amount(level, tech=1, res=None):
    """Wood or stone amount depend on level."""
    result = (
        (1 / math.e**(level - ZERO_EXPONENT) + RES_TIME_COEF)
        * level ** RES_EXPONENT_COEF
    ) * res / tech
    return int(result)


if __name__ == '__main__':
    for i in range(1, 51):
        print(int(get_resources_amount(i, 1, 10)))
