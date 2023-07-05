from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ...towns.models import Fraction

User = get_user_model()


class TestViews(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.fraction = Fraction.objects.create(
            name='TestFraction',
            bonus='Test bonus',
            description='test description',
            slug='test_slug',
        )
        cls.user = User.objects.create_user(
            username='Test_User',
            fraction=TestViews.fraction,
        )
        cls.urls_template = (
            (reverse('users:signup'), 'users/signup.html'),
            (reverse('users:login'), 'users/login.html'),
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(TestViews.user)

    def test_used_templates(self):
        """Check used templates."""
        for address, template in TestViews.urls_template:
            with self.subTest(view=address):
                response = self.guest_client.get(address)
                self.assertTemplateUsed(response, template)

    def test_check_context_signup_page(self):
        """Check context of Signup page."""
        response = self.guest_client.get(reverse('users:signup'))
        fractions = response.context.get('fractions')
        self.assertEqual(fractions[0].id, TestViews.fraction.id)
