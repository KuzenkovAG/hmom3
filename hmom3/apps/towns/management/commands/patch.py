import csv

from django.conf import settings
from django.core.management.base import BaseCommand

from ....towns import models


class Command(BaseCommand):
    help = "Patch new fraction to existing DB."

    def handle(self, *args, **options):
        if settings.DEBUG:
            static = settings.STATICFILES_DIRS[0]
        else:
            static = settings.STATIC_ROOT

        files = [
            (models.Fraction, f'{static}/data/patch_fraction.csv'),
            (models.Building, f'{static}/data/patch_buildings.csv'),
            (
                models.BuildingRequirement,
                f'{static}/data/patch_building_requirements.csv'
            ),
        ]

        for model, file in files:

            data = []

            with open(file, encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile, delimiter=';')
                for line in reader:
                    row = model(**line)
                    data.append(row)

            created_objects = model.objects.bulk_create(data)
            created_count = len(created_objects)
            self.stdout.write(
                self.style.SUCCESS(
                    f'({model}) Создано записей: {created_count}'
                )
            )
