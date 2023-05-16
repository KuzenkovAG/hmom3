from django.shortcuts import get_object_or_404
from django.utils import timezone
from . import models


def get_and_update_resources(user):
    """Get resources of User and Update it."""
    resources = user.resource
    resources.update_data()
    return resources


def get_finish_time(duration):
    """Calculate build finish time."""
    return timezone.now() + duration


def _create_building(building_in_process, user):
    """
    Increase building level. Remove requirements if needed.
    """
    user_building = get_object_or_404(
        models.UserBuilding, id=building_in_process.building.id)
    user_building.save(level_up=True)
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
