from django.urls import path, reverse_lazy
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordChangeDoneView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)

from . import views
from apps.core.decorators import for_not_authorized

app_name = 'users'

urlpatterns = [
    path('signup/',
         for_not_authorized(views.UserCreationView.as_view()),
         name='signup'),
    path('',
         for_not_authorized(LoginView.as_view(
            template_name='users/login.html',
         )),
         name='login'),
    path('logout/',
         LogoutView.as_view(
             template_name='users/logout.html',
             next_page=reverse_lazy('users:login')
         ),
         name='logout'),
    path('password_change/',
         PasswordChangeView.as_view(
             template_name='users/password_change.html',
             success_url='done/'
         ),
         name='password_change'),
    path('password_change/done/',
         PasswordChangeDoneView.as_view(
             template_name='users/password_change_done.html',
         ),
         name='password_change_done'),
    path('password_reset/',
         PasswordResetView.as_view(
             template_name='users/password_reset.html',
             email_template_name='users/password_reset_email.html',
             success_url=reverse_lazy('users:password_reset_done'),
         ),
         name='password_reset'),
    path('password_reset/done/',
         PasswordResetDoneView.as_view(
             template_name='users/password_reset_done.html',
         ),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(
             template_name='users/password_change.html',
             success_url=reverse_lazy('users:password_reset_complete')
         ),
         name='password_reset_confirm'),
    path('reset/done/',
         PasswordResetCompleteView.as_view(
             template_name='users/password_change_done.html',
         ),
         name='password_reset_complete'),
]
