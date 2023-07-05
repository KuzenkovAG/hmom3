from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ...towns import models

User = get_user_model()


class ViewTest(TestCase):
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
            fraction=ViewTest.castle,
        )
        cls.urls_template = (
            ('/statics/', 'stats/index.html'),
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(ViewTest.user)

    def test_template_used(self):
        """Check template used."""
        for url, template in ViewTest.urls_template:
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertTemplateUsed(response, template)

    def test_context_index(self):
        """Check context of index page."""
        resources = models.Resource.objects.get(user=ViewTest.user)
        response = self.authorized_client.get(reverse('stats:index'))
        resources_context = response.context.get('resources')
        self.assertEqual(resources, resources_context)
