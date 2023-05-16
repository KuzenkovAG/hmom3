from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'towns'

urlpatterns = [
    path('',
         login_required(views.TownView.as_view()),
         name='index'),
    path('build/',
         login_required(views.BuildView.as_view()),
         name='build'),
    path('build/<str:building>/',
         login_required(views.ConstructBuildView.as_view()),
         name='construct_build'),
    path('research/',
         login_required(views.ResearchView.as_view()),
         name='research'),
    path('army/',
         login_required(views.ArmyView.as_view()),
         name='army'),
    ]
