from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView

from ..towns import utils
from .forms import TradeForm
from .utils import trade_resources

GOLD_PER_WOOD = settings.GOLD_PER_WOOD
GOLD_PEF_STONE = settings.GOLD_PEF_STONE
WOOD_PER_GOLD = settings.WOOD_PER_GOLD
STONE_PER_GOLD = settings.STONE_PER_GOLD
WOOD_PER_STONE = settings.WOOD_PER_STONE
STONE_PER_WOOD = settings.STONE_PER_WOOD

User = get_user_model()


class MarketView(FormView):
    """Market page for trade resources."""
    template_name = 'market/index.html'
    form_class = TradeForm
    success_url = reverse_lazy('market:index')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        user = get_object_or_404(
            User.objects.select_related('fraction'),
            username=self.request.user.username
        )
        show = user.buildings.filter(
            building__type__name='market',
            level__gt=0
        ).exists()
        context['show'] = show
        context['resources'] = utils.get_and_update_resources(user)
        context['gold_per_wood'] = GOLD_PER_WOOD
        context['gold_per_stone'] = GOLD_PEF_STONE
        context['wood_per_gold'] = WOOD_PER_GOLD
        context['wood_per_stone'] = WOOD_PER_STONE
        context['stone_per_gold'] = STONE_PER_GOLD
        context['stone_per_wood'] = STONE_PER_WOOD
        return context

    def form_valid(self, form):
        trade_resources(
            from_r=form.cleaned_data.get('from_resource'),
            to_r=form.cleaned_data.get('to_resource'),
            value=int(form.cleaned_data.get('value')),
            user=self.request.user
        )
        return redirect(self.success_url)
