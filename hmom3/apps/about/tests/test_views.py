from django.contrib.auth import get_user_model
from django.test import Client, TestCase

User = get_user_model()


class ViewTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.urls_template = (
            ('/about/', 'about/index.html'),
        )

    def setUp(self):
        self.guest_client = Client()

    def test_template_used(self):
        """Check template used."""
        for url, template in ViewTest.urls_template:
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertTemplateUsed(response, template)
