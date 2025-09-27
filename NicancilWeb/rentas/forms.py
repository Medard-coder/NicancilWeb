from django import forms
from .models import Renta, Cliente

class RentaForm(forms.ModelForm):
    class Meta:
        model = Renta
        fields = ['cliente', 'fecha_inicio', 'fecha_fin', 'ine_entregada']
        widgets = {
            'fecha_inicio': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'fecha_fin': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'cliente': forms.Select(attrs={'class': 'form-select'}),
            'ine_entregada': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'telefono', 'correo', 'direccion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
    
    def clean_nombre(self):
        nombre = self.cleaned_data['nombre']
        # Verificar si ya existe un cliente con el mismo nombre (sin importar mayúsculas/minúsculas)
        if Cliente.objects.filter(nombre__iexact=nombre).exists():
            raise forms.ValidationError('Ya existe un cliente con este nombre.')
        return nombre