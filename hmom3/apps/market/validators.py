from django.core.exceptions import ValidationError

AVAILABLE_RESOURCES = {'gold', 'wood', 'stone'}


def validate_resource(value):
    """Validate available resources."""
    if value not in AVAILABLE_RESOURCES:
        raise ValidationError('Ресурс указан неверно.')
