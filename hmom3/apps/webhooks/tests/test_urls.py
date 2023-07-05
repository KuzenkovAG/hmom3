from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase

User = get_user_model()


class AvailableURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.urls = (
            '/hooks/pull/',
        )

    def setUp(self):
        self.guest_client = Client()

    def test_urls_status_code(self):
        """Check status code for wrong request."""
        for url in AvailableURLTests.urls:
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
