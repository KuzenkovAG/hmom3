from django.urls import path, reverse_lazy
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'towns'

urlpatterns = [
    path('',
         login_required(views.TownView.as_view()),
         name='index'),
    ]
