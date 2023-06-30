from django.conf import settings
from django.core.management.base import BaseCommand

from ....core.balance.resources import get_resource_income, get_resource_limit
from ....towns import models

DEF_GOLD_INCOME = settings.DEF_GOLD_INCOME
DEF_WOOD_INCOME = settings.DEF_WOOD_INCOME
DEF_STONE_INCOME = settings.DEF_STONE_INCOME
DEF_GOLD_LIMIT = settings.DEF_GOLD_LIMIT
DEF_STONE_LIMIT = settings.DEF_STONE_LIMIT
DEF_WOOD_LIMIT = settings.DEF_WOOD_LIMIT


class Command(BaseCommand):
    help = "Patch what correct resources of existing Users."

    def handle(self, *args, **options):
        resources = models.Resource.objects.all()

        for resource in resources:
            sild = models.UserBuilding.objects.filter(
                user=resource.user.id).filter(building__type__name='sild')
            hall = models.UserBuilding.objects.filter(
                user=resource.user.id).filter(building__type__name='hall')

            if sild.exists() and sild[0].level != 0:
                resource.gold_limit = get_resource_limit(
                    sild[0].level,
                    resource='gold'
                )
                resource.wood_limit = get_resource_limit(
                    sild[0].level,
                    resource='wood'
                )
                resource.stone_limit = resource.wood_limit
            else:
                resource.gold_limit = DEF_GOLD_LIMIT
                resource.wood_limit = DEF_WOOD_LIMIT
                resource.stone_limit = DEF_STONE_LIMIT

            if hall.exists() and hall[0].level != 0:
                resource.gold_income = get_resource_income(
                    hall[0].level,
                    resource='gold'
                )
            else:
                resource.gold_income = DEF_GOLD_INCOME
            resource.wood_income = DEF_WOOD_INCOME
            resource.stone_income = DEF_STONE_INCOME

            resource.save()

        print('Users resources updated.')
