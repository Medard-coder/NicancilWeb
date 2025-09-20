from django import forms
from .models import Cita
from rentas.models import Cliente

class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['cliente', 'fecha_cita', 'motivo', 'estado']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'fecha_cita': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'motivo': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'cliente': 'Cliente',
            'fecha_cita': 'Fecha y Hora de la Cita',
            'motivo': 'Motivo de la Cita',
            'estado': 'Estado',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cliente'].queryset = Cliente.objects.all().order_by('nombre')