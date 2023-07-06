"""
Define function of increasing amount depend on building level:
 - Building time
 - Research time
"""
import math

BUILD_TIME_COEF = 0.08
SEARCH_TIME_COEF = 0.2
BUILD_EXPONENT_COEF = 3
SEARCH_EXPONENT_COEF = 2
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


if __name__ == '__main__':
    for i in range(1, 101):
        print(int(get_research_time(i, 1, 1)))
