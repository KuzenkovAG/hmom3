from ..towns.views import ViewWithContext


class StatisticView(ViewWithContext):
    template_name = 'stats/index.html'
