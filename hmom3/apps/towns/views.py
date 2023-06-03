from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import RedirectView

from .models import UserBuilding, BuildingInProcess
from . import utils
from ..core.views import ViewWithContext


class TownView(ViewWithContext):
    template_name = 'towns/town.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        user = context['user']
        buildings = user.buildings.select_related(
            'building', 'building__type').all()
        context['buildings'] = buildings
        context['build_in_process'] = utils.get_building_in_process(user)
        return context


class BuildView(ViewWithContext):
    template_name = 'towns/build.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        user = context['user']
        user_build = user.buildings.select_related(
            'building__type',
            'building__fraction',
        ).prefetch_related(
            'user_building__requirement__fraction'
        ).all()
        context['user_build'] = user_build
        context['build_in_process'] = utils.get_building_in_process(user)
        return context


class ArmyView(ViewWithContext):
    template_name = 'towns/army.html'


class ResearchView(ViewWithContext):
    template_name = 'towns/research.html'


class ConstructBuildView(RedirectView):
    url = reverse_lazy('towns:build')

    def get(self, request, *args, **kwargs):
        user = self.request.user
        if not BuildingInProcess.objects.filter(user=user).exists():
            slug = f"{user.fraction.slug[:1]}-{kwargs.get('building')}"
            building = get_object_or_404(UserBuilding, user=user, slug=slug)
            # check requirements
            if building.level > 0 or not building.user_building.all():
                resource = utils.get_and_update_resources(user)
                resource_condition = (
                        building.gold <= resource.gold_amount and
                        building.wood <= resource.wood_amount and
                        building.stone <= resource.stone_amount
                )
                if resource_condition:
                    resource.gold_amount -= building.gold
                    resource.wood_amount -= building.wood
                    resource.stone_amount -= building.stone
                    resource.save()
                    BuildingInProcess.objects.create(
                        user=user,
                        building=building,
                        finish_date=utils.get_finish_time(
                            building.building_time)
                    )
        return super().get(request, *args, **kwargs)
