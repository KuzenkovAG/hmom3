from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from django.views.generic import TemplateView

User = get_user_model()


class TownView(TemplateView):
    template_name = 'towns/town.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        user = get_object_or_404(User, id=self.request.user.id)
        context['resources'] = user.resource.all()

        buildings = user.buildingscompleted.all()
        return context
