from django.db import models
from django.urls import reverse

class Prenda(models.Model):
    TIPOS = (
        ('traje', 'Traje'),
        ('vestido', 'Vestido'),
        ('accesorio', 'Accesorio'),
    )
    ESTATUS = (
        ('disponible', 'Disponible'),
        ('apartado', 'Apartado'),
        ('en_uso', 'En Uso'),
        ('dañado', 'Dañado'),
        ('mantenimiento', 'En Mantenimiento'),
        ('lavanderia', 'En Lavandería'),
    )
    GENEROS = (
        ('hombre', 'Hombre'),
        ('mujer', 'Mujer'),
        ('unisex', 'Unisex'),
    )
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    tipo = models.CharField(max_length=20, choices=TIPOS, default='traje')
    color = models.CharField(max_length=50, blank=True)
    estatus = models.CharField(max_length=20, choices=ESTATUS, default='disponible')
    tallas = models.CharField(max_length=50, blank=True)
    genero = models.CharField(max_length=10, choices=GENEROS, default='unisex')
    lugar = models.CharField(max_length=100, blank=True, verbose_name="Lugar o sitio del traje")
    cantidad = models.PositiveIntegerField(default=1)
    imagen = models.ImageField(upload_to='prendas/', null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('prenda_detalle', args=[str(self.id)])