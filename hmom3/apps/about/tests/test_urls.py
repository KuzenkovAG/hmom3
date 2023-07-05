from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

User = get_user_model()


class AvailableURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.urls_redirect_quest = (
            ('/about/', reverse('users:login')),
        )

    def setUp(self):
        self.guest_client = Client()

    def test_urls_status_code(self):
        """Check status code for authorized user."""
        for url, _ in AvailableURLTests.urls_redirect_quest:
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)
