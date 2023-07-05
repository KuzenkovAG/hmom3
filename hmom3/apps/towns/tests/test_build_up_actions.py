import datetime as dt

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ...towns import models

User = get_user_model()


class BuildingLevelUpTest(TestCase):
    """Tests cases when building gain level up."""
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.castle = models.Fraction.objects.create(
            name='Замок',
            bonus='Test bonus',
            description='test description',
            slug='castle',
        )
        # create types
        cls.hall = models.BuildingType.objects.create(
            name='hall',
            order=1,
            base_time=dt.timedelta(minutes=0),
            base_gold=2,
            base_wood=1,
            base_stone=1
        )
        cls.sild = models.BuildingType.objects.create(
            name='sild',
            order=2,
            base_time=dt.timedelta(minutes=0),
            base_gold=2,
            base_wood=1,
            base_stone=1
        )
        # create buildings
        cls.hall_castle = models.Building.objects.create(
            name='Капитолий',
            description='Капитолий замка',
            type=BuildingLevelUpTest.hall,
            fraction=BuildingLevelUpTest.castle,
            slug='c-hall'
        )
        cls.sild_castle = models.Building.objects.create(
            name='Таверна',
            description='Таверна замка',
            type=BuildingLevelUpTest.sild,
            fraction=BuildingLevelUpTest.castle,
            slug='c-sild'
        )
        cls.user = User.objects.create(
            username='Test_User',
            fraction=BuildingLevelUpTest.castle,
            password='pass_word'
        )

    def setUp(self):
        self.resources = models.Resource.objects.get(
            user=BuildingLevelUpTest.user
        )
        self.authorized_client = Client()
        self.authorized_client.force_login(BuildingLevelUpTest.user)

    def test_create_hall(self):
        """After creation gold income should be increase."""
        gold_before = self.resources.gold_income
        self.authorized_client.get(reverse(
            'towns:construct_build', args=[BuildingLevelUpTest.hall.name]
        ))
        self.authorized_client.get(reverse('towns:build'))
        resources = models.Resource.objects.get(user=BuildingLevelUpTest.user)
        self.assertTrue(
            resources.gold_income > gold_before,
            "Gold income changed not correctly"
        )

    def test_create_slid(self):
        """After creation resource limit should be increased"""
        gold_limit_before = self.resources.gold_limit
        wood_limit_before = self.resources.wood_limit
        stone_limit_before = self.resources.stone_limit
        self.authorized_client.get(reverse(
            'towns:construct_build', args=[BuildingLevelUpTest.sild.name]
        ))
        self.authorized_client.get(reverse('towns:build'))
        resources = models.Resource.objects.get(user=BuildingLevelUpTest.user)
        self.assertTrue(
            resources.gold_limit > gold_limit_before,
            "Gold limit changed not correctly"
        )
        self.assertTrue(
            resources.wood_limit > wood_limit_before,
            "Wood limit changed not correctly"
        )
        self.assertTrue(
            resources.stone_limit > stone_limit_before,
            "Stone limit changed not correctly"
        )
