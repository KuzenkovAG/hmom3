from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (AuthenticationForm, UserCreationForm,
                                       UsernameField)
from django.utils.translation import ugettext_lazy as _

User = get_user_model()


class CreationForm(UserCreationForm):
    """Form for user registration."""
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'fraction')
        labels = {
            'username': _('Логин'),
            'email': _('Почта'),
        }
        widgets = {
            'fraction': forms.HiddenInput(),
        }


class LoginForm(AuthenticationForm):
    """Form for login user."""
    username = UsernameField(
        widget=forms.TextInput(attrs={'autofocus': True}),
        label='Логин'
    )
