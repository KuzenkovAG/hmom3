from ..towns import models


def create_resources(user):
    """Create entries in db - resources."""
    models.Resource.objects.create(user=user)


def create_buildings(user):
    """Create entries in db - buildings."""
    buildings = models.Building.objects.select_related(
        'type').filter(fraction=user.fraction)

    objects = [
        models.UserBuilding(
            user=user,
            building=building,
            level=0,
            building_time=building.type.base_time,
            gold=building.type.base_gold,
            wood=building.type.base_wood,
            stone=building.type.base_stone,
            slug=building.slug
        ) for building in buildings
    ]
    models.UserBuilding.objects.bulk_create(objects)


def create_requirements(user):
    """Create entries in db - requirements."""
    objects = user.buildings.all()
    requirment_objects = []

    for obj in objects:
        requirements = models.BuildingRequirement.objects.filter(
            building=obj.building)

        for requirement in requirements:
            obj2 = models.UserBuildingRequirement(
                    building=obj,
                    requirement=requirement.requirement,
                    level=requirement.level,
                )
            requirment_objects.append(obj2)

    models.UserBuildingRequirement.objects.bulk_create(requirment_objects)


def set_up_user(user):
    """Create entries in db for user."""
    create_resources(user)
    create_buildings(user)
    create_requirements(user)
