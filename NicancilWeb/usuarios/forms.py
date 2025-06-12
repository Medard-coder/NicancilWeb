# usuarios/forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class RegistroForm(UserCreationForm):
    class Meta:
        model=Usuario
        fields = ['email', 'rol', 'password1', 'password2']
        widgets = {
            'email': forms.EmailInput(attrs={"class": "form-control"}),
            'rol': forms.Selec(attrs={"class": "form-control"}),
        }