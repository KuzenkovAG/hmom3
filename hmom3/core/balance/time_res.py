"""
Define function of increasing amount depend on level:
 - Building time
 - Research time;
 - Gold amount;
 - Resources (wood, stone) amount.
"""

import datetime as dt
import math

levels = range(1, 51)
INITIAL_TIME = dt.timedelta(0, 0, 0, 0, 1)
INITIAL_SEARCH_TIME = dt.timedelta(0, 0, 0, 0, 0, 1)
INITIAL = 200
re = INITIAL/100

BUILD_TIME_COEF = 2/25
SEARCH_TIME_COEF = 1/5
RES_TIME_COEF = 1/5
GOLD_TIME_COEF = 1/2

BUILD_EXPONENT_COEF = 3
SEARCH_EXPONENT_COEF = 2
RES_EXPONENT_COEF = 2.5
GOLD_EXPONENT_COEF = 4

ZERO_EXPONENT = 1


def building_time(level, tech=1, time=None):
    """Building time depend on level."""
    result = ((1 / math.e ** (level - ZERO_EXPONENT) + 1 * BUILD_TIME_COEF)
              * level ** BUILD_EXPONENT_COEF) * time / tech
    return result


def research_time(level, tech=1, time=None):
    """Research time depend on level."""
    result = (
        (1 / math.e ** (level - ZERO_EXPONENT) + SEARCH_TIME_COEF) *
        level ** SEARCH_EXPONENT_COEF
    ) * time / tech
    return result


def gold_amount(level, tech=1, res=None):
    """Gold amount depend on level."""
    result = (
        (1 / math.e ** (level - ZERO_EXPONENT) + GOLD_TIME_COEF) *
        level ** GOLD_EXPONENT_COEF
    ) * res / tech
    return int(result)


def res_amount(level, tech=1, res=None):
    """Wood or stone amount depend on level."""
    result = (
        (1 / math.e ** (level - ZERO_EXPONENT) + RES_TIME_COEF) *
        level ** RES_EXPONENT_COEF
    ) * res / tech
    return int(result)


if __name__ == '__main__':
    for level in levels:
        print(
            level,
            gold_amount(level, 1, INITIAL),
            res_amount(level, 1, INITIAL/100)
        )
