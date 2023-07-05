from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ...towns import models
from ..forms import TradeForm

User = get_user_model()

GOLD_PER_WOOD = settings.GOLD_PER_WOOD
GOLD_PEF_STONE = settings.GOLD_PEF_STONE
WOOD_PER_GOLD = settings.WOOD_PER_GOLD
WOOD_PER_STONE = settings.WOOD_PER_STONE
STONE_PER_GOLD = settings.STONE_PER_GOLD
STONE_PER_WOOD = settings.STONE_PER_WOOD


class FormTest(TestCase):
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
            fraction=FormTest.castle,
        )
        cls.ok_data = {
            'from_resource': 'gold',
            'to_resource': 'wood',
            'value': WOOD_PER_GOLD
        }
        cls.wrong_value_data = {
            'from_resource': 'gold',
            'to_resource': 'wood',
            'value': 'one hundred'
        }
        cls.wrong_zero_value_data = {
            'from_resource': 'gold',
            'to_resource': 'wood',
            'value': '0'
        }
        cls.wrong_from_data = {
            'from_resource': 'голда',
            'to_resource': 'wood',
            'value': 150
        }
        cls.wrong_to_data = {
            'from_resource': 'gold',
            'to_resource': 'дерево',
            'value': 150
        }
        cls.wrong_same_from_to_data = {
            'from_resource': 'gold',
            'to_resource': 'gold',
            'value': 150
        }

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(FormTest.user)

    def test_trade_gold_to_wood(self):
        """Testcase - trade is success."""
        resources = models.Resource.objects.get(user=FormTest.user)
        gold_before = round(resources.gold_amount, 0)
        wood_before = round(resources.wood_amount, 0)
        self.authorized_client.post(
            reverse('market:index'),
            data=FormTest.ok_data,
        )
        gold_removed = FormTest.ok_data.get('value')
        wood_added = round(FormTest.ok_data.get('value') / WOOD_PER_GOLD, 0)
        resources_after = models.Resource.objects.get(user=FormTest.user)
        self.assertEqual(
            gold_before - gold_removed,
            round(resources_after.gold_amount, 0),
            'Was removed not correct gold amount'
        )
        self.assertEqual(
            wood_before + wood_added,
            round(resources_after.wood_amount, 0),
            'Was removed not correct wood amount'
        )

    def test_wrong_value_data(self):
        """Value is not number."""
        form = TradeForm(data=FormTest.wrong_value_data)
        self.assertFalse(form.is_valid())
        error = form.errors.get('__all__')
        self.assertIn('Значение должно быть указано числом.', error)

    def test_zero_value_data(self):
        """Value is zero."""
        form = TradeForm(data=FormTest.wrong_zero_value_data)
        self.assertFalse(form.is_valid())
        error = form.errors.get('__all__')
        self.assertIn('Укажите не нулевое значение.', error)

    def test_wrong_from_data(self):
        """From resource have wrong format."""
        form = TradeForm(data=FormTest.wrong_from_data)
        self.assertFalse(form.is_valid())
        error = form.errors.get('__all__')
        self.assertIn('Не указан ресурс.', error)

    def test_wrong_to_data(self):
        """To resource have wrong format."""
        form = TradeForm(data=FormTest.wrong_to_data)
        self.assertFalse(form.is_valid())
        error = form.errors.get('__all__')
        self.assertIn('Не указан ресурс.', error)

    def test_wrong_data_same_resources(self):
        """Same resources for trading."""
        form = TradeForm(data=FormTest.wrong_same_from_to_data)
        self.assertFalse(form.is_valid())
        error = form.errors.get('__all__')
        self.assertIn('Для обмена выберете разные ресурсы.', error)
