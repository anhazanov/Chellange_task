from django.contrib.auth.forms import AuthenticationForm
from django import forms


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='username', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='some_password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
