from django import template

register = template.Library()


@register.filter
def addclass(field, css):
    """Add HTML attribute 'class' to field."""
    return field.as_widget(attrs={'class': css})


@register.filter(name='times')
def times(number):
    return range(number)
