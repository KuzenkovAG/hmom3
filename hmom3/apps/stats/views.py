from apps.towns.views import TemplateViewWithContext


class StatisticView(TemplateViewWithContext):
    template_name = 'stats/index.html'
