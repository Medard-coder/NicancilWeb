from django.db import models
from django.urls import reverse

class Prenda(models.Model):
    TIPOS = (
        ('traje', 'Traje'),
        ('vestido', 'Vestido'),
        ('accesorio', 'Accesorio'),
    )
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    tipo = models.CharField(max_length=20, choices=TIPOS, default='traje')
    imagen = models.ImageField(upload_to='prendas/', null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('prenda_detalle', args=[str(self.id)])