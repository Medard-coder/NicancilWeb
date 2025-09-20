from django.db import models
from rentas.models import Cliente

class Cita(models.Model):
    ESTADOS = (
        ('pendiente', 'Pendiente'),
        ('realizada', 'Realizada'),
        ('cancelada', 'Cancelada'),
    )
    
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='citas')
    fecha_cita = models.DateTimeField()
    motivo = models.TextField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Cita"
        verbose_name_plural = "Citas"
        ordering = ['-fecha_cita']
    
    def __str__(self):
        return f"Cita {self.id} - {self.cliente.nombre} - {self.fecha_cita.strftime('%d/%m/%Y %H:%M')}"