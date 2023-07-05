from django.core.exceptions import ValidationError
from django.test import TestCase

from ..validators import validate_resource


class ValidatorTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.wrong_resource = 'wrong'
        cls.ok_resource = ('gold', 'wood', 'stone')

    def test_ok_resource(self):
        """Check if resource is ok."""
        for resource in ValidatorTest.ok_resource:
            with self.subTest(resource=resource):
                validate_resource(resource)

    def test_wrong_resource(self):
        """Raise Validation error if name is wrong."""
        with self.assertRaises(
                ValidationError,
                msg='Validator pass wrong name.'
        ):
            validate_resource(ValidatorTest.wrong_resource)
