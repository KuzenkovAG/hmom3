from django.shortcuts import render
from django.contrib.auth import get_user_model, login
from django.views.generic import CreateView
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy

from towns.models import Fractions
from . import forms

User = get_user_model()


class UserCreationView(CreateView):
    form_class = forms.CreationForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/signup.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['fractions'] = Fractions.objects.all()
        return context

    def form_valid(self, form):
        form.save()
        username = self.request.POST['username']
        user = get_object_or_404(User, username=username)
        login(self.request, user)
        return redirect(self.success_url)
