from django import forms
from .models import Prenda, PrendaVariante

class PrendaForm(forms.ModelForm):
    class Meta:
        model = Prenda
        fields = ['nombre', 'precio', 'tipo', 'descripcion', 'color', 'estatus', 'tallas', 'genero', 'lugar', 'cantidad','imagen']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control'}),
            'estatus': forms.Select(attrs={'class': 'form-control'}),
            'tallas': forms.TextInput(attrs={'class': 'form-control'}),
            'genero': forms.Select(attrs={'class': 'form-control'}),
            'lugar': forms.TextInput(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'imagen': forms.FileInput(attrs={'class': 'form-control'}),
        }

class PrendaVarianteForm(forms.ModelForm):
    class Meta:
        model = PrendaVariante
        fields = ['color', 'talla', 'cantidad', 'estatus', 'imagen']
        widgets = {
            'color': forms.TextInput(attrs={'class': 'form-control'}),
            'talla': forms.TextInput(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'estatus': forms.Select(attrs={'class': 'form-control'}),
            'imagen': forms.FileInput(attrs={'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        self.prenda = kwargs.pop("prenda", None)
        super().__init__(*args, **kwargs)
        
    def clean(self):
        cleaned_data = super().clean()
        color = cleaned_data.get("color")
        talla = cleaned_data.get("talla")
        
        if self.prenda and color and talla:
            existe=PrendaVariante.objects.filter(
                prenda=self.prenda,
                color=color,
                talla=talla
            ).exists()
            
            if existe:
                raise forms.ValidationError("Ya existe una variante con el mismo color y talla.")
            return cleaned_data