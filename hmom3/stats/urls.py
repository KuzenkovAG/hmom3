from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'stats'

urlpatterns = [
    path('',
         login_required(views.StatisticView.as_view()),
         name='index'),
    ]
