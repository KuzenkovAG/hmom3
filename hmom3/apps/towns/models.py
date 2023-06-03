from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.conf import settings
from django.urls import reverse

from ..core.balance.duration_cost import get_building_time

User = get_user_model()

SEC_IN_HOUR = 3600
BUILDINGS_WITH_CHANGE_IMAGE = settings.BUILDINGS_WITH_CHANGE_IMAGE

DEF_GOLD_AMOUNT = settings.DEF_GOLD_AMOUNT
DEF_WOOD_AMOUNT = settings.DEF_WOOD_AMOUNT
DEF_STONE_AMOUNT = settings.DEF_STONE_AMOUNT
DEF_GOLD_INCOME = settings.DEF_GOLD_INCOME
DEF_WOOD_INCOME = settings.DEF_WOOD_INCOME
DEF_STONE_INCOME = settings.DEF_STONE_INCOME
DEF_GOLD_LIMIT = settings.DEF_GOLD_LIMIT
DEF_STONE_LIMIT = settings.DEF_STONE_LIMIT
DEF_WOOD_LIMIT = settings.DEF_WOOD_LIMIT


BUILDING_URL = {
    'hall': 'towns:build',
    'market': 'market:index',
}


class Fraction(models.Model):
    """Information about fraction."""
    name = models.CharField(max_length=20, verbose_name='Название')
    bonus = models.CharField(max_length=256, verbose_name='Бонус')
    description = models.CharField(max_length=512, verbose_name='Описание')
    slug = models.CharField(max_length=20, verbose_name='Slug', unique=True)

    def __str__(self):
        return self.slug

    class Meta:
        verbose_name = 'Фракция'
        verbose_name_plural = 'Фракции'


class Resource(models.Model):
    """Current users resources."""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name='Ресурсы',
        related_name='resource',
    )
    gold_amount = models.FloatField(default=DEF_GOLD_AMOUNT)
    wood_amount = models.FloatField(default=DEF_WOOD_AMOUNT)
    stone_amount = models.FloatField(default=DEF_STONE_AMOUNT)
    gold_income = models.IntegerField(default=DEF_GOLD_INCOME)
    wood_income = models.IntegerField(default=DEF_WOOD_INCOME)
    stone_income = models.IntegerField(default=DEF_STONE_INCOME)
    updated_time = models.DateTimeField(auto_now_add=True)
    gold_limit = models.BigIntegerField(default=DEF_GOLD_LIMIT)
    wood_limit = models.BigIntegerField(default=DEF_STONE_LIMIT)
    stone_limit = models.BigIntegerField(default=DEF_WOOD_LIMIT)

    class Meta:
        verbose_name = 'Ресурсы'
        verbose_name_plural = 'Ресурсы'

    def update_data(self):
        """Update all resources."""
        time_now_utc = timezone.now()
        time_difference = time_now_utc - self.updated_time
        sec_passed = time_difference.total_seconds()
        self.gold_amount += sec_passed * self.gold_income / SEC_IN_HOUR
        self.wood_amount += sec_passed * self.wood_income / SEC_IN_HOUR
        self.stone_amount += sec_passed * self.stone_income / SEC_IN_HOUR

        self._check_limits()
        self.updated_time = time_now_utc
        self.save()

    def _check_limits(self):
        """Check resources limits."""
        if self.gold_amount > self.gold_limit:
            self.gold_amount = self.gold_limit
        if self.wood_amount > self.wood_limit:
            self.wood_amount = self.wood_limit
        if self.stone_amount > self.stone_limit:
            self.stone_amount = self.stone_limit


class BuildingType(models.Model):
    """Base Building types."""
    name = models.CharField(max_length=32, verbose_name='Название')
    order = models.SmallIntegerField('Порядок', null=True, blank=True)
    base_time = models.DurationField(null=True, blank=True)
    base_gold = models.SmallIntegerField('Золото')
    base_wood = models.SmallIntegerField('Дерево')
    base_stone = models.SmallIntegerField('Камень')

    class Meta:
        verbose_name = 'Тип строения'
        verbose_name_plural = 'Типы строений'
        ordering = ('order',)

    def __str__(self):
        return self.name

    def get_build_time(self, level):
        return get_building_time(level=level, time=self.base_time)


class BuildingRequirement(models.Model):
    """Base Requirements for buildings."""
    building = models.ForeignKey(
        'Building',
        on_delete=models.CASCADE,
        verbose_name='Здание',
        null=True,
        blank=True
    )
    requirement = models.ForeignKey(
        'Building',
        on_delete=models.CASCADE,
        verbose_name='Требование',
        related_name='requirements',
        null=True,
        blank=True,
    )
    level = models.SmallIntegerField(default=1)

    class Meta:
        verbose_name = 'Требования к постройкам'
        verbose_name_plural = 'Требования к постройкам'
        ordering = ('building', 'requirement')

    def __str__(self):
        return f'{self.building} - {self.requirement} lv.{self.level}'


class Building(models.Model):
    """Information about all buildings."""
    name = models.CharField(max_length=32, verbose_name='Название')
    description = models.TextField(
        max_length=512,
        verbose_name='Описание',
        null=True,
        blank=True
    )
    type = models.ForeignKey(
        BuildingType,
        on_delete=models.SET_NULL,
        related_name='types',
        verbose_name='Тип',
        null=True,
        blank=True
    )
    fraction = models.ForeignKey(
        Fraction,
        on_delete=models.CASCADE,
        verbose_name='Фракция',
    )
    slug = models.CharField(max_length=32,)

    def __str__(self):
        return f'{self.fraction} {self.name}'

    class Meta:
        verbose_name = 'Строения'
        verbose_name_plural = 'Строения'
        ordering = ('type',)
        constraints = [
            models.UniqueConstraint(
                fields=['type', 'fraction'],
                name='unique_type_fraction'
            )
        ]


class UserBuilding(models.Model):
    """Which buildings users have."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='buildings',
    )
    building = models.ForeignKey(
        Building,
        on_delete=models.CASCADE,
        verbose_name='строение',
        related_name='user_buildings',
    )
    level = models.SmallIntegerField('уровень')
    building_time = models.DurationField(null=True, blank=True)
    gold = models.BigIntegerField('Золото')
    wood = models.BigIntegerField('Дерево')
    stone = models.BigIntegerField('Stone')
    slug = models.CharField(max_length=32,)

    class Meta:
        verbose_name = 'Построенные здания'
        verbose_name_plural = 'Построенные здания'
        ordering = ('building',)
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'building'],
                name='unique_user_building'
            )
        ]

    def __str__(self):
        return f'{self.building} {self.user.username}'

    def get_absolute_url(self):
        """Depend on building generate related url."""
        name_space = BUILDING_URL.get(self.slug[2:])
        if name_space:
            return reverse(name_space)
        return ''

    def get_index(self) -> str:
        """
        Get index for buildings what need change image.
        """
        calculate_index = BUILDINGS_WITH_CHANGE_IMAGE.get(
            self.slug.split('-')[1])
        index = str(calculate_index(self.level + 1)) if calculate_index else ''
        return index


class BuildingInProcess(models.Model):
    """What buildings currently users makes."""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='buildings2'
    )
    building = models.ForeignKey(
        'UserBuilding',
        on_delete=models.CASCADE,
        verbose_name='Строения'
    )
    finish_date = models.DateTimeField()

    class Meta:
        verbose_name = 'Строящиеся здания'
        verbose_name_plural = 'Строящиеся здания'

    def is_finished(self):
        return self.finish_date <= timezone.now()

    def get_duration(self):
        return self.finish_date - timezone.now()


class UserBuildingRequirement(models.Model):
    """Requirements for buildings, what have user."""
    building = models.ForeignKey(
        'UserBuilding',
        on_delete=models.CASCADE,
        verbose_name='Здание',
        related_name='user_building'
    )
    requirement = models.ForeignKey(
        'Building',
        on_delete=models.CASCADE,
        verbose_name='Требование',
        related_name='user_requirements'
    )
    level = models.SmallIntegerField(default=1)

    class Meta:
        verbose_name = 'Требования для зданий построенные игроком'
        verbose_name_plural = 'Требования для зданий построенные игроком'
        ordering = ('building', 'requirement')

    def __str__(self):
        return f'{self.building} - {self.requirement} lv.{self.level}'
