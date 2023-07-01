from django.urls import path

from . import views

app_name = 'webhooks'

urlpatterns = [
    path('pull/', views.pull_repo, name='pull'),
]
