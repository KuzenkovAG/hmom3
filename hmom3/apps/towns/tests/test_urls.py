import datetime as dt
from http import HTTPStatus

from apps.towns import models
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

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
        cls.hall = models.BuildingType.objects.create(
            name='hall',
            order=1,
            base_time=dt.timedelta(minutes=1),
            base_gold=1000,
            base_wood=10,
            base_stone=10
        )
        cls.hall_castle = models.Building.objects.create(
            name='Капитолий',
            description='Капитолий замка',
            type=AvailableURLTests.hall,
            fraction=AvailableURLTests.castle,
            slug='c-hall'
        )
        cls.user = User.objects.create_user(
            username='Test_User',
            fraction=cls.castle,
        )
        cls.urls_template = (
            ('/town/', 'towns/town.html'),
            ('/town/build/', 'towns/build.html'),
            ('/town/research/', 'towns/research.html'),
            ('/town/army/', 'towns/army.html'),
        )
        cls.urls_redirect_authorized = (
            ('/town/build/hall/', reverse('towns:build')),
        )
        cls.urls_redirect_quest = (
            ('/town/', reverse('users:login')),
            ('/town/build/', reverse('users:login')),
            ('/town/research/', reverse('users:login')),
            ('/town/army/', reverse('users:login')),
            ('/town/build/hall/', reverse('users:login')),
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_urls_authorized_user_ok_status(self):
        """Check status code for authorized user."""
        for url, _ in AvailableURLTests.urls_template:
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_urls_authorized_user_redirect(self):
        """Check redirect of authorized user."""
        for url, redirect_url in AvailableURLTests.urls_redirect_authorized:
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertRedirects(response, redirect_url)

    def test_urls_guest_user_ok_status(self):
        """Check status code for guest user."""
        for url, _ in AvailableURLTests.urls_redirect_quest:
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_urls_guest_user_redirect(self):
        """Check redirect of guest user."""
        for url, redirect_url in AvailableURLTests.urls_redirect_quest:
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                redirect_url += '?next=' + url
                self.assertRedirects(response, redirect_url)

    def test_template_for_urls(self):
        """Check correct used template."""
        for url, template in AvailableURLTests.urls_template:
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertTemplateUsed(response, template)
