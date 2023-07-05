import datetime as dt

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

from ...towns import models

User = get_user_model()


class TestViews(TestCase):
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
            type=TestViews.hall,
            fraction=TestViews.castle,
            slug='c-hall'
        )
        cls.user = User.objects.create(
            username='Test_User',
            fraction=TestViews.castle,
            password='pass_word'
        )
        user_building = models.UserBuilding.objects.get(
            user=TestViews.user,
            building=TestViews.hall_castle
        )
        cls.build_in_process = models.BuildingInProcess.objects.create(
            user=TestViews.user,
            building=user_building,
            finish_date=timezone.now() + dt.timedelta(minutes=1)
        )
        cls.urls_template = (
            (reverse('towns:index'), 'towns/town.html'),
            (reverse('towns:build'), 'towns/build.html'),
            (reverse('towns:research'), 'towns/research.html'),
            (reverse('towns:army'), 'towns/army.html'),
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(TestViews.user)

    def test_template_for_urls(self):
        """Check used template."""
        for url, template in TestViews.urls_template:
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertTemplateUsed(response, template)

    def test_check_context_town(self):
        """Check context of town page."""
        response = self.authorized_client.get(reverse('towns:index'))

        # resources
        resources = models.Resource.objects.get(user=TestViews.user)
        resources_context = response.context.get('resources')
        self.assertEqual(resources, resources_context)

        # buildings
        buildings = models.UserBuilding.objects.get(user=TestViews.user)
        buildings_context = response.context.get('buildings')
        self.assertEqual(buildings.id, buildings_context[0].id)

        # buildings in process
        build_in_process_context = response.context.get('build_in_process')
        self.assertEqual(TestViews.build_in_process, build_in_process_context)

    def test_check_context_build(self):
        """Check context of build page."""
        response = self.authorized_client.get(reverse('towns:build'))

        # resources
        resources = models.Resource.objects.get(user=TestViews.user)
        resources_context = response.context.get('resources')
        self.assertEqual(resources, resources_context)

        # buildings
        buildings = models.UserBuilding.objects.get(user=TestViews.user)
        buildings_context = response.context.get('user_build')
        self.assertEqual(buildings.id, buildings_context[0].id)

        # buildings in process
        build_in_process_context = response.context.get('build_in_process')
        self.assertEqual(TestViews.build_in_process, build_in_process_context)


class CreateBuilding(TestCase):
    """Tests for create building."""
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
            base_time=dt.timedelta(minutes=0),
            base_gold=10,
            base_wood=5,
            base_stone=5
        )
        cls.tavern = models.BuildingType.objects.create(
            name='tavern',
            order=2,
            base_time=dt.timedelta(minutes=0),
            base_gold=10,
            base_wood=5,
            base_stone=5
        )
        cls.hall_castle = models.Building.objects.create(
            name='Капитолий',
            description='Капитолий замка',
            type=CreateBuilding.hall,
            fraction=CreateBuilding.castle,
            slug='c-hall'
        )
        cls.tavern_castle = models.Building.objects.create(
            name='Таверна',
            description='Таверна замка',
            type=CreateBuilding.tavern,
            fraction=CreateBuilding.castle,
            slug='c-tavern'
        )
        models.BuildingRequirement.objects.create(
            building=CreateBuilding.tavern_castle,
            requirement=CreateBuilding.hall_castle,
            level=1
        )

        cls.user = User.objects.create(
            username='Test_User',
            fraction=CreateBuilding.castle,
            password='pass_word'
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(CreateBuilding.user)

    def test_create_building(self):
        """
        Resources reduce after start building.
        After finishing level of building increase.
        Cost of gold, wood, stone also increase.
        Requirements removed.
        """
        # initialize creation building
        res_before = models.Resource.objects.get(user=CreateBuilding.user)
        self.authorized_client.get(
            reverse('towns:construct_build', args=[CreateBuilding.hall.name])
        )
        res_after = models.Resource.objects.get(user=CreateBuilding.user)
        gold = res_after.gold_amount + CreateBuilding.hall.base_gold
        wood = res_after.wood_amount + CreateBuilding.hall.base_wood
        stone = res_after.stone_amount + CreateBuilding.hall.base_stone
        self.assertEqual(
            round(res_before.gold_amount, 0),
            round(gold, 0),
            'Gold reduced on wrong amount'
        )
        self.assertEqual(
            round(res_before.wood_amount, 0),
            round(wood, 0),
            'Wood reduced on wrong amount'
        )
        self.assertEqual(
            round(res_before.stone_amount, 0),
            round(stone, 0),
            'Stone reduced on wrong amount'
        )
        self.assertNotEqual(
            res_before.gold_amount,
            gold,
            'Resources not calculated'
        )
        user_hall = models.UserBuilding.objects.get(
            user=CreateBuilding.user,
            building=CreateBuilding.hall_castle
        )
        initial_level = user_hall.level
        initial_gold = user_hall.gold
        initial_wood = user_hall.wood
        initial_stone = user_hall.stone
        user_tavern = models.UserBuilding.objects.get(
            user=CreateBuilding.user,
            building=CreateBuilding.tavern_castle,
        )
        requirements = models.UserBuildingRequirement.objects.filter(
            building=user_tavern,
            requirement=CreateBuilding.hall_castle
        )
        self.assertTrue(
            requirements.exists(),
            'Requirement not exist.'
        )
        # finish creation building
        self.authorized_client.get(reverse('towns:build'))
        user_hall = models.UserBuilding.objects.get(
            user=CreateBuilding.user,
            building=CreateBuilding.hall_castle
        )
        self.assertEqual(
            initial_level + 1,
            user_hall.level,
            'Level not increased'
        )
        self.assertNotEqual(
            initial_gold,
            user_hall.gold,
            'Gold not increased.'
        )
        self.assertNotEqual(
            initial_stone,
            user_hall.stone,
            'Stone not increased.'
        )
        self.assertNotEqual(
            initial_wood,
            user_hall.wood,
            'Wood not increased.'
        )
        # check removed requirements
        requirements = models.UserBuildingRequirement.objects.filter(
            building=user_tavern,
            requirement=CreateBuilding.hall_castle
        )
        self.assertFalse(
            requirements.exists(),
            'Requirement not removed.'
        )


class CantCreateBuilding(TestCase):
    """Tests cases when building can't be created."""
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
            base_gold=10,
            base_wood=50,
            base_stone=5
        )
        cls.tavern = models.BuildingType.objects.create(
            name='tavern',
            order=2,
            base_time=dt.timedelta(minutes=0),
            base_gold=10,
            base_wood=5,
            base_stone=5
        )
        cls.sild = models.BuildingType.objects.create(
            name='sild',
            order=2,
            base_time=dt.timedelta(minutes=1),
            base_gold=10,
            base_wood=5,
            base_stone=5
        )
        # create buildings
        cls.hall_castle = models.Building.objects.create(
            name='Капитолий',
            description='Капитолий замка',
            type=CantCreateBuilding.hall,
            fraction=CantCreateBuilding.castle,
            slug='c-hall'
        )
        cls.tavern_castle = models.Building.objects.create(
            name='Таверна',
            description='Таверна замка',
            type=CantCreateBuilding.tavern,
            fraction=CantCreateBuilding.castle,
            slug='c-tavern'
        )
        cls.sild_castle = models.Building.objects.create(
            name='Таверна',
            description='Таверна замка',
            type=CantCreateBuilding.sild,
            fraction=CantCreateBuilding.castle,
            slug='c-sild'
        )
        # create requirements
        models.BuildingRequirement.objects.create(
            building=CantCreateBuilding.tavern_castle,
            requirement=CantCreateBuilding.hall_castle,
            level=1
        )
        cls.user = User.objects.create(
            username='Test_User',
            fraction=CantCreateBuilding.castle,
            password='pass_word'
        )

    def setUp(self):
        models.BuildingInProcess.objects.filter(
            user=CantCreateBuilding.user,
        ).delete()
        self.authorized_client = Client()
        self.authorized_client.force_login(CantCreateBuilding.user)

    def test_not_enough_resources(self):
        """Can't build if resources not enough."""
        self.authorized_client.get(
            reverse(
                'towns:construct_build',
                args=[CantCreateBuilding.hall.name]
            )
        )
        build_in_process = models.BuildingInProcess.objects.filter(
            user=CantCreateBuilding.user,
        )
        self.assertFalse(
            build_in_process.exists(),
            'Can not building if resources not enough.'
        )

    def test_not_enough_requirements(self):
        """Can't build when requirements exists."""
        self.authorized_client.get(
            reverse(
                'towns:construct_build',
                args=[CantCreateBuilding.tavern.name]
            )
        )
        build_in_process = models.BuildingInProcess.objects.filter(
            user=CantCreateBuilding.user,
        )
        self.assertFalse(
            build_in_process.exists(),
            'Can not building if have requirements.'
        )

    def test_build_only_one_building(self):
        """Can build only one building in any time."""
        for _ in range(2):
            self.authorized_client.get(
                reverse(
                    'towns:construct_build',
                    args=[CantCreateBuilding.sild.name]
                )
            )
            buildings_created = models.BuildingInProcess.objects.filter(
                user=CantCreateBuilding.user,
            ).count()
            self.assertEqual(
                buildings_created,
                1,
                'Can create only one building.'
            )
