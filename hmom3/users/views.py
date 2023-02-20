from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.views.generic import CreateView

User = get_user_model()


class UserCreationView(CreateView):
    model = User
    fields = ('login', 'email')
