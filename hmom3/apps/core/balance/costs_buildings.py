"""
Define function of increasing amount depend on building level:
Cost of buildings
"""


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
