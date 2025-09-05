from django.db import models
from inventario.models import PrendaUnidad

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    correo = models.EmailField()
    direccion = models.TextField()
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre

class Renta(models.Model):
    ESTADOS = (
        ('activa', 'Activa'),
        ('finalizada', 'Finalizada'),
    )
    
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='rentas')
    prendas = models.ManyToManyField(PrendaUnidad, related_name='rentas')
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='activa')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Renta"
        verbose_name_plural = "Rentas"
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"Renta {self.id} - {self.cliente.nombre}"