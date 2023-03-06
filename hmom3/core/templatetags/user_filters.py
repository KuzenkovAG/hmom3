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
    return int(number)
