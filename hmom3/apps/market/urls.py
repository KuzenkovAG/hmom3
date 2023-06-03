from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'market'

urlpatterns = [
    path('',
         login_required(views.MarketView.as_view()),
         name='index'),
    path('trade/',
         login_required(views.TradeView.as_view()),
         name='trade'),
    ]
