import datetime as dt

from apps.towns import models
from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class UserCreationTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.castle = models.Fraction.objects.create(
            name='Castle',
            bonus='Test bonus',
            description='test description',
            slug='castle',
        )
        cls.inferno = models.Fraction.objects.create(
            name='Inferno',
            bonus='Test bonus',
            description='test description',
            slug='inferno',
        )
        cls.hall = models.BuildingType.objects.create(
            name='hall',
            order=1,
            base_time=dt.timedelta(minutes=1),
            base_gold=1000,
            base_wood=10,
            base_stone=10
        )
        cls.tavern = models.BuildingType.objects.create(
            name='tavern',
            order=2,
            base_time=dt.timedelta(minutes=1),
            base_gold=1000,
            base_wood=10,
            base_stone=10
        )
        cls.hall_castle = models.Building.objects.create(
            name='Капитолий',
            description='Капитолий замка',
            type=UserCreationTest.hall,
            fraction=UserCreationTest.castle,
            slug='c-hall'
        )
        cls.hall_inferno = models.Building.objects.create(
            name='Капитолий',
            description='Капитолий инферно',
            type=UserCreationTest.hall,
            fraction=UserCreationTest.inferno,
            slug='i-hall'
        )
        cls.tavern_castle = models.Building.objects.create(
            name='Таверна',
            description='Таверна замка',
            type=UserCreationTest.tavern,
            fraction=UserCreationTest.castle,
            slug='c-tavern'
        )
        models.BuildingRequirement.objects.create(
            building=UserCreationTest.tavern_castle,
            requirement=UserCreationTest.hall_castle,
            level=1,
        )
        cls.user = User.objects.create_user(
            username='castle_user',
            password='easy_password',
            fraction=UserCreationTest.castle,
        )

    def test_resources(self):
        """Created user have resources and amount is correct."""
        resources = models.Resource.objects.filter(user=UserCreationTest.user)
        self.assertTrue(
            resources.exists(),
            'Created User do not have resources.'
        )
        resources = resources[0]
        self.assertEqual(resources.gold_income, 50)
        self.assertEqual(resources.wood_income, 3)
        self.assertEqual(resources.stone_income, 3)
        self.assertEqual(resources.gold_limit, 1000)
        self.assertEqual(resources.wood_limit, 20)
        self.assertEqual(resources.stone_limit, 20)
        self.assertEqual(resources.gold_amount, 500)
        self.assertEqual(resources.wood_amount, 15)
        self.assertEqual(resources.stone_amount, 15)

    def test_buildings(self):
        """Created user have buildings."""
        user_buildings = models.UserBuilding.objects.filter(
            user=UserCreationTest.user
        )
        self.assertTrue(user_buildings.exists(), 'User do not have buildings.')
        self.assertEqual(user_buildings.count(), 2)

    def test_requirements(self):
        """Created user have requirements for buildings."""
        user_tavern = models.UserBuilding.objects.get(
            user=UserCreationTest.user,
            building=UserCreationTest.tavern_castle,
        )
        user_requirements = models.UserBuildingRequirement.objects.filter(
            building=user_tavern
        )
        self.assertTrue(
            user_requirements.exists(),
            'User do not have requirements for buildings'
        )
