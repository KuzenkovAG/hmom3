from django import template
from django.template.defaultfilters import floatformat

register = template.Library()


@register.filter
def addclass(field, css):
    """Add HTML attribute 'class' to field."""
    return field.as_widget(attrs={'class': css})


@register.filter(name='times')
def times(number):
    """For cycle."""
    return range(number)


@register.filter(name='my_float')
def my_float(float_number):
    """Float format with '.' separator."""
    return floatformat(float_number, arg=-1).replace(',', '.')


@register.filter(name='round_down')
def round_down(number):
    """Round number down."""
    if isinstance(number, str):
        return number
    return int(number)


@register.filter(name='is_even')
def is_even(number):
    """Chech number is even or not."""
    if number % 2 == 0:
        return True
    return False


@register.filter(name='split_half')
def split_half(number):
    """Split number in half."""
    return int(number / 2)


@register.simple_tag
def get_slug(object, level):
    """Run method get_slug."""
    return object.get_slug(level)


@register.simple_tag
def define(val=None):
    """Define variable."""
    return val


@register.filter(name='time_format')
def time_format(duration):
    """Remove microseconds from timedelta format."""
    days, seconds = duration.days, duration.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = (seconds % 60)
    return f'{hours:02d}:{minutes:02d}:{seconds:02d}'
