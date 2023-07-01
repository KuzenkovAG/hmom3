from django.conf import settings
from django.core.management.base import BaseCommand

from ....core.balance.duration_cost import get_gold_amount
from ....core.balance.resources import get_resource_income
from ....towns import models

DEF_GOLD_INCOME = settings.DEF_GOLD_INCOME
DEF_WOOD_INCOME = settings.DEF_WOOD_INCOME
DEF_STONE_INCOME = settings.DEF_STONE_INCOME
DEF_GOLD_LIMIT = settings.DEF_GOLD_LIMIT
DEF_STONE_LIMIT = settings.DEF_STONE_LIMIT
DEF_WOOD_LIMIT = settings.DEF_WOOD_LIMIT


class Command(BaseCommand):
    help = "Patch what correct resources of existing Users and building cost."

    def handle(self, *args, **options):

        # пересчет поступаемого золота для всех игроков
        resources = models.Resource.objects.all()

        for resource in resources:
            hall = models.UserBuilding.objects.filter(
                user=resource.user.id).filter(building__type__name='hall')

            if hall.exists() and hall[0].level != 0:
                resource.gold_income = get_resource_income(
                    hall[0].level,
                    resource='gold'
                )
            else:
                resource.gold_income = DEF_GOLD_INCOME
            resource.save()
        print('Users resources updated.')

        # пересчет стоимости всех зданий для всех игроков
        buildings = models.UserBuilding.objects.select_related(
            'building__type'
        ).all()

        for user_building in buildings:
            user_building.gold = get_gold_amount(
                level=user_building.level + 1,
                tech=1,
                res=user_building.building.type.base_gold
            )
            user_building.save()
        print('Building costs updated.')
