import datetime as dt

from django.test import TestCase

from ..balance import costs_buildings, duration, resources


class CostTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.tech = 1
        cls.gold_init = 50
        cls.costs_gold = (
            (1, 70),
            (10, 17500),
            (20, 150000),
            (30, 750000),
        )
        cls.resources_init = 5
        cls.costs_resources = (
            (1, 6),
            (10, 99),
            (20, 1000),
            (30, 4998),
        )

    def test_gold_amount(self):
        """Check costs of gold depend on level."""
        for level, cost in CostTest.costs_gold:
            with self.subTest(level=level, cost=cost):
                result = costs_buildings.get_gold_amount(
                    level,
                    CostTest.tech,
                    CostTest.gold_init
                )
                self.assertEqual(result, cost)

    def test_resources_amount(self):
        """Check costs of resources depend on level."""
        for level, cost in CostTest.costs_resources:
            with self.subTest(level=level, cost=cost):
                result = costs_buildings.get_resources_amount(
                    level,
                    CostTest.tech,
                    CostTest.resources_init
                )
                self.assertEqual(result, cost)


class ResourcesTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.tech = 1
        cls.gold_limit = 1000
        cls.resource_limit = 20
        cls.gold_income = 50
        cls.level_limits_gold = (
            (0, ResourcesTest.gold_limit),
            (1, 1500),
            (10, 50000),
            (20, 500000),
            (30, 5000300)
        )
        cls.level_limits_resources = (
            (0, ResourcesTest.resource_limit),
            (1, 30),
            (10, 1000),
            (20, 10000),
            (30, 100006)
        )
        cls.level_income_gold = (
            (0, ResourcesTest.gold_income),
            (1, 58),
            (10, 391),
            (20, 958),
            (30, 3025)
        )

    def test_gold_limits(self):
        """Check limits of golds depend on level."""
        for level, limit in ResourcesTest.level_limits_gold:
            with self.subTest(level=level, limit=limit):
                result = resources.get_resource_limit(
                    level,
                    ResourcesTest.tech,
                    'gold'
                )
                self.assertEqual(result, limit)

    def test_resources_limits(self):
        """Check resources of golds depend on level."""
        for level, limit in ResourcesTest.level_limits_resources:
            with self.subTest(level=level, limit=limit):
                result = resources.get_resource_limit(
                    level,
                    ResourcesTest.tech,
                    'wood'
                )
                self.assertEqual(result, limit)

    def test_gold_income(self):
        """Check income of golds depend on level."""
        for level, income in ResourcesTest.level_income_gold:
            with self.subTest(level=level, income=income):
                result = resources.get_resource_income(
                    level,
                    ResourcesTest.tech,
                    'gold'
                )
                self.assertEqual(result, income)


class BuildsDurationTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.tech = 1
        cls.base_duration = dt.timedelta(minutes=1)
        cls.level_durations = (
            (1, dt.timedelta(seconds=64, microseconds=800000)),
            (10, dt.timedelta(seconds=4807, microseconds=404588)),
            (20, dt.timedelta(seconds=38400, microseconds=2689)),
            (30, dt.timedelta(days=1, seconds=43200))
        )

    def test_buildings_duration(self):
        """Check duration of buildings depend on level."""
        for level, value in BuildsDurationTest.level_durations:
            with self.subTest(level=level, value=value):
                result = duration.get_building_time(
                    level,
                    BuildsDurationTest.tech,
                    BuildsDurationTest.base_duration
                )
                self.assertEqual(result, value)
