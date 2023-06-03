from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from ..towns import utils

User = get_user_model()


class ViewWithContext(TemplateView):
    """Add some data to context."""
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        user = get_object_or_404(
            User.objects.select_related('fraction'),
            username=self.request.user.username
        )
        context['user'] = user
        context['resources'] = utils.get_and_update_resources(user)
        return context
