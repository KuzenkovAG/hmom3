from django.shortcuts import get_object_or_404
from django.utils import timezone

from ..core.balance import costs_buildings, duration
from . import models
from .action import building_level_up

ACTION_ON_LEVEL_UP = {
    'hall': building_level_up.create_hall,
    'sild': building_level_up.create_slid,
}


def get_and_update_resources(user):
    """Get resources of User and Update it."""
    resources = user.resource
    resources.update_data()
    return resources


def get_finish_time(duration):
    """Calculate build finish time."""
    return timezone.now() + duration


def _level_up(instance):
    """Increase level."""
    instance.level += 1
    build_time = instance.building.type.base_time
    base_gold = instance.building.type.base_gold
    base_wood = instance.building.type.base_wood
    base_stone = instance.building.type.base_stone
    instance.building_time = duration.get_building_time(
        level=instance.level, time=build_time)
    instance.gold = costs_buildings.get_gold_amount(
        level=instance.level,
        res=base_gold
    )
    instance.wood = costs_buildings.get_resources_amount(
        level=instance.level,
        res=base_wood
    )
    instance.stone = costs_buildings.get_resources_amount(
        level=instance.level, res=base_stone
    )
    instance.save()


def _create_building(building_in_process, user):
    """
    Increase building level.
    Do some action depend on building.
    Remove requirements if needed.
    """
    user_building = get_object_or_404(
        models.UserBuilding.objects.select_related('building__type'),
        id=building_in_process.building.id
    )
    _level_up(user_building)
    action = ACTION_ON_LEVEL_UP.get(user_building.building.type.name)
    if action:
        action(user=user, user_building=user_building)
    building_in_process.delete()

    models.UserBuildingRequirement.objects.filter(
        building__user=user,
        requirement=user_building.building,
        level=user_building.level
    ).delete()


def get_building_in_process(user):
    """Get building what making now."""
    building_in_process = models.BuildingInProcess.objects.select_related(
        'building').filter(user=user)
    exists = building_in_process.exists()
    if exists and building_in_process[0].is_finished():
        return _create_building(building_in_process[0], user)
    return building_in_process[0] if exists else None
