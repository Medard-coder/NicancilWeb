from django import forms
from .models import Prenda

class PrendaForm(forms.ModelForm):
    class Meta:
        model = Prenda
        fields = ['nombre', 'precio', 'tipo', 'descripcion', 'imagen']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'imagen': forms.FileInput(attrs={'class': 'form-control'}),
        }