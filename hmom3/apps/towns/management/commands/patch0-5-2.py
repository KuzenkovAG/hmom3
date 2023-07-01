from django.conf import settings
from django.core.management.base import BaseCommand

from ....core.balance import duration_cost
from ....towns import models

DEF_GOLD_INCOME = settings.DEF_GOLD_INCOME
DEF_WOOD_INCOME = settings.DEF_WOOD_INCOME
DEF_STONE_INCOME = settings.DEF_STONE_INCOME
DEF_GOLD_LIMIT = settings.DEF_GOLD_LIMIT
DEF_STONE_LIMIT = settings.DEF_STONE_LIMIT
DEF_WOOD_LIMIT = settings.DEF_WOOD_LIMIT


class Command(BaseCommand):
    help = "Patch what correct building cost."

    def handle(self, *args, **options):

        # пересчет стоимости всех зданий для всех игроков
        buildings = models.UserBuilding.objects.select_related(
            'building__type'
        ).all()

        for user_building in buildings:
            user_building.gold = duration_cost.get_gold_amount(
                level=user_building.level + 1,
                tech=1,
                res=user_building.building.type.base_gold
            )
            user_building.wood = duration_cost.get_resources_amount(
                level=user_building.level + 1,
                tech=1,
                res=user_building.building.type.base_wood
            )
            user_building.stone = duration_cost.get_resources_amount(
                level=user_building.level + 1,
                tech=1,
                res=user_building.building.type.base_stone
            )
            user_building.save()
        print('Building costs updated.')
