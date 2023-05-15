import csv
import datetime as dt

from django.core.management.base import BaseCommand

from towns import models


class Command(BaseCommand):
    help = "Fill DB for major data."

    def handle(self, *args, **options):
        files = [
            (models.Fraction, r'hmom3/static/data/fractions.csv'),
            (models.BuildingType, r'hmom3/static/data/buildings_type.csv'),
            (models.Building, r'hmom3/static/data/buildings.csv'),
            (
                models.BuildingRequirement,
                r'hmom3/static/data/building_requirements.csv'
            ),
        ]

        for model, file in files:
            object_model = model.objects.all()
            object_model.delete()
            data = []

            with open(file, encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile, delimiter=';')
                for line in reader:
                    row = model(**line)
                    data.append(row)

            if hasattr(data[0], 'base_time'):
                for d in data:
                    d.base_time = dt.timedelta(microseconds=int(d.base_time))

            created_objects = model.objects.bulk_create(data)
            created_count = len(created_objects)
            self.stdout.write(
                self.style.SUCCESS(
                    f'({model}) Создано записей: {created_count}'
                )
            )