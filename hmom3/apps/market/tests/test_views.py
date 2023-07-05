from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ...towns import models

User = get_user_model()

GOLD_PER_WOOD = settings.GOLD_PER_WOOD
GOLD_PEF_STONE = settings.GOLD_PEF_STONE
WOOD_PER_GOLD = settings.WOOD_PER_GOLD
WOOD_PER_STONE = settings.WOOD_PER_STONE
STONE_PER_GOLD = settings.STONE_PER_GOLD
STONE_PER_WOOD = settings.STONE_PER_WOOD


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
            (reverse('market:index'), 'market/index.html'),
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
        response = self.authorized_client.get(reverse('market:index'))
        resources_context = response.context.get('resources')
        self.assertEqual(resources, resources_context)

        show = models.UserBuilding.objects.filter(
            user=self.user,
            building__type__name='market'
        ).exists()
        show_context = response.context.get('show')
        self.assertEqual(show, show_context)

        # trade coefficients
        gold_wood_context = response.context.get('gold_per_wood')
        gold_stone_context = response.context.get('gold_per_stone')
        wood_gold_context = response.context.get('wood_per_gold')
        wood_stone_context = response.context.get('wood_per_stone')
        stone_gold_context = response.context.get('stone_per_gold')
        stone_wood_context = response.context.get('stone_per_wood')
        self.assertEqual(gold_wood_context, GOLD_PER_WOOD)
        self.assertEqual(gold_stone_context, GOLD_PER_WOOD)
        self.assertEqual(wood_gold_context, WOOD_PER_GOLD)
        self.assertEqual(wood_stone_context, WOOD_PER_STONE)
        self.assertEqual(stone_gold_context, STONE_PER_GOLD)
        self.assertEqual(stone_wood_context, STONE_PER_WOOD)
