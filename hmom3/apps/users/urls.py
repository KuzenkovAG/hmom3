from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, reverse_lazy

from ..core.decorators import for_not_authorized
from . import forms, views

app_name = 'users'

urlpatterns = [
    path(
        'signup/',
        for_not_authorized(views.UserCreationView.as_view()),
        name='signup'
    ),
    path(
        '',
        for_not_authorized(LoginView.as_view(
            form_class=forms.LoginForm,
            template_name='users/login.html',
        )),
        name='login'
    ),
    path(
        'logout/',
        LogoutView.as_view(
            template_name='users/logout.html',
            next_page=reverse_lazy('users:login')
        ),
        name='logout'
    ),
]
