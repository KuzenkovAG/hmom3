from http import HTTPStatus

from apps.towns.models import Fraction
from django.contrib.auth import get_user_model
from django.test import Client, TestCase

User = get_user_model()


class AvailableURLTests(TestCase):
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
            fraction=cls.fraction,
        )
        cls.urls_template = (
            ('/town/', 'users/login.html'),
            ('/town/build/', 'users/signup.html'),
            ('/town/research/', 'users/signup.html'),
            ('/town/army/', 'users/signup.html'),
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_urls_OK_status(self):
        """Check status code for guest URLs."""
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        response = self.guest_client.get('/signup/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_urls_redirects(self):
        """Check status code for guest URLs."""
        response = self.guest_client.get('/logout/')
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        response = self.authorized_client.get('/')
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_url_unexisting_page(self):
        """Unexisting page should have NOT_FOUND status code."""
        response = self.authorized_client.get('/unexisting_page/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_url_used_template(self):
        """Check correct template for pages."""
        for url, template in AvailableURLTests.urls_template:
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertTemplateUsed(response, template)
