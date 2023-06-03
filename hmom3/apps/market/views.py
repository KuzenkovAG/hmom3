from django.views.generic import RedirectView
from ..core.views import ViewWithContext


class MarketView(ViewWithContext):
    template_name = 'market/index.html'


class TradeView(RedirectView):
    pass
