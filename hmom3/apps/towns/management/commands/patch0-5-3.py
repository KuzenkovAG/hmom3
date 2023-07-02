from django.conf import settings
from django.core.management.base import BaseCommand

from ....core.balance import resources
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

        # пересчет лимитов ресурсов игроков
        resources_obj = models.Resource.objects.all()

        for resource in resources_obj:
            slid = models.UserBuilding.objects.filter(
                user=resource.user).filter(building__type__name='sild')

            if slid.exists():
                resource.gold_limit = resources.get_resource_limit(
                    slid[0].level,
                    resource='gold'
                )
                resource.wood_limit = resources.get_resource_limit(
                    slid[0].level,
                    resource='wood'
                )
                resource.stone_limit = resources.get_resource_limit(
                    slid[0].level,
                    resource='stone'
                )

            else:
                resource.gold_limit = DEF_GOLD_LIMIT
                resource.wood_limit = DEF_WOOD_LIMIT
                resource.stone_limit = DEF_STONE_LIMIT
            resource.save()
        print('Users resources updated.')
