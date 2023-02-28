from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime
from django.utils import timezone

User = get_user_model()
SEC_IN_HOUR = 3600


class Fractions(models.Model):
    name = models.CharField(max_length=20, verbose_name='Название')
    bonus = models.CharField(max_length=256, verbose_name='Бонус')
    description = models.CharField(max_length=512, verbose_name='Описание')
    image = models.ImageField(
        'Картинка',
        upload_to='fractions/',
        blank=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Фракция'
        verbose_name_plural = 'Фракции'


class Resources(models.Model):
    user = models.ForeignKey(
        User,
        'Ресурсы',
        related_name='resource'
    )
    gold_amount = models.FloatField(default=100)
    wood_amount = models.FloatField(default=50)
    stone_amount = models.FloatField(default=50)
    gold_income = models.IntegerField(default=0)
    wood_income = models.IntegerField(default=0)
    stone_income = models.IntegerField(default=0)
    updated_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Ресурсы'
        verbose_name_plural = 'Ресурсы'

    def update_data(self):
        time_now_utc = timezone.now()
        time_difference = time_now_utc - self.updated_time
        sec_passed = time_difference.total_seconds()
        self.gold_amount += sec_passed * self.gold_income / SEC_IN_HOUR
        self.wood_amount += sec_passed * self.wood_income / SEC_IN_HOUR
        self.stone_amount += sec_passed * self.stone_income / SEC_IN_HOUR
        self.updated_time = time_now_utc
        self.save()

    def set_all_zero(self):
        self.gold_amount = 0
        self.wood_amount = 0
        self.stone_amount = 0
        self.updated_time = timezone.now()
        self.save()
