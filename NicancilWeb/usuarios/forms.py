# usuarios/forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={"class": "form-control"}))
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={"class": "form-control"}))
    
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'password1', 'password2']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.rol = 'emp'  # Forzar rol de empleado
        if commit:
            user.save()
        return user

class EditarPerfilForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'email', 'telefono', 'foto_perfil']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellidos'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de teléfono'}),
            'foto_perfil': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellidos',
            'email': 'Correo electrónico',
            'telefono': 'Teléfono',
            'foto_perfil': 'Foto de perfil',
        }