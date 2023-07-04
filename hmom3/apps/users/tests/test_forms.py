from apps.towns import models
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

User = get_user_model()


class FormTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.fraction = models.Fraction.objects.create(
            name='TestFraction',
            bonus='Test bonus',
            description='test description',
            slug='test_slug',
        )
        cls.user = User.objects.create_user(
            username='Test_User',
            password='easy_password',
            fraction=cls.fraction,
        )
        cls.login_data = {
            'username': 'Test_User',
            'password': 'easy_password'
        }
        cls.signup_data = {
            'username': 'Test_User2',
            'email': 'test2@mail.ru',
            'password1': 'easy_password',
            'password2': 'easy_password',
            'fraction': cls.fraction.id,
        }

    def setUp(self):
        self.guest_client = Client()

    def test_login_form(self):
        """Check successful login."""
        response = self.guest_client.post(
            reverse('users:login'),
            data=FormTest.login_data,
            folow=True,
        )
        self.assertRedirects(response, reverse('towns:index'))

    def test_signup_form(self):
        """Check creation user."""
        users_count = User.objects.count()
        response = self.guest_client.post(
            reverse('users:signup'),
            data=FormTest.signup_data,
            folow=True,
        )
        self.assertEqual(User.objects.count(), users_count + 1)
        self.assertRedirects(response, reverse('towns:index'))
        self.assertTrue(
            User.objects.filter(
                username='Test_User2',
                email='test2@mail.ru',
                fraction=FormTest.fraction.id,
            ).exists(),
            'User created not correct.'
        )
