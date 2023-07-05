import datetime as dt

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from ...towns import models

User = get_user_model()

GOLD_LIMIT = settings.DEF_GOLD_LIMIT
WOOD_LIMIT = settings.DEF_WOOD_LIMIT
STONE_LIMIT = settings.DEF_STONE_LIMIT


class TestModels(TestCase):
    """Tests of views."""
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.castle = models.Fraction.objects.create(
            name='Замок',
            bonus='Test bonus',
            description='test description',
            slug='castle',
        )
        cls.hall = models.BuildingType.objects.create(
            name='hall',
            order=1,
            base_time=dt.timedelta(minutes=1),
            base_gold=10,
            base_wood=1,
            base_stone=1
        )
        cls.hall_castle = models.Building.objects.create(
            name='Капитолий',
            description='Капитолий замка',
            type=TestModels.hall,
            fraction=TestModels.castle,
            slug='c-hall'
        )
        cls.user = User.objects.create(
            username='Test_User',
            fraction=TestModels.castle,
            password='pass_word'
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(TestModels.user)

    def test_resource_limit(self):
        """Resources amount should not more than limits."""
        resources = models.Resource.objects.get(user=TestModels.user)
        resources.gold_amount = GOLD_LIMIT * 2
        resources.wood_amount = WOOD_LIMIT * 2
        resources.stone_amount = STONE_LIMIT * 2
        resources.update_data()
        self.assertEqual(resources.gold_amount, GOLD_LIMIT)
        self.assertEqual(resources.wood_amount, WOOD_LIMIT)
        self.assertEqual(resources.stone_amount, STONE_LIMIT)
