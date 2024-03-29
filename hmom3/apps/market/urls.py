from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

app_name = 'market'

urlpatterns = [
    path('', login_required(views.MarketView.as_view()), name='index'),
]
