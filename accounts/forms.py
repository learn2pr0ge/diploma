from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from allauth.account.forms import LoginForm
from django.utils.translation import gettext_lazy as _
from allauth.account.forms import SignupForm

class LoginForm(AuthenticationForm):
    error_messages = {
        'invalid_login': _(
            "Неверный логин или пароль. "
            "Убедитесь, что раскладка клавиатуры верна и CAPS LOCK выключен."
        ),
        'inactive': _("Этот аккаунт неактивен."),
    }

    username = forms.CharField(label="Имя пользователя")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)

class NoSignupForm(SignupForm):
    def is_open_for_signup(self, request):
        return False


