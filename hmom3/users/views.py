from django.contrib.auth import get_user_model, login
from django.views.generic import CreateView
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy

from towns.models import Fraction
from . import forms
from . import utils

User = get_user_model()


class UserCreationView(CreateView):
    """Create user."""
    form_class = forms.CreationForm
    success_url = reverse_lazy('towns:index')
    template_name = 'users/signup.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['fractions'] = Fraction.objects.all()
        return context

    def form_valid(self, form):
        form.save()
        username = self.request.POST['username']
        user = get_object_or_404(User, username=username)
        utils.set_up_user(user)
        login(self.request, user)
        return redirect(self.success_url)
