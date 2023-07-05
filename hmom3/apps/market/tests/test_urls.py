from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ...towns import models

User = get_user_model()


class AvailableURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.castle = models.Fraction.objects.create(
            name='Castle',
            bonus='Test bonus',
            description='test description',
            slug='castle',
        )
        cls.user = User.objects.create_user(
            username='Test_User',
            fraction=AvailableURLTests.castle,
        )
        cls.urls_redirect_quest = (
            ('/market/', reverse('users:login')),
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(AvailableURLTests.user)

    def test_urls_guest_redirect(self):
        """Check redirect for guest user."""
        for url, redirect in AvailableURLTests.urls_redirect_quest:
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                redirect += '?next=' + url
                self.assertRedirects(response, redirect)

    def test_urls_authorized_user(self):
        """Check status code for authorized user."""
        for url, _ in AvailableURLTests.urls_redirect_quest:
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)
