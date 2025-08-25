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

class PrendaVariante(models.Model):
    prenda = models.ForeignKey(Prenda, on_delete=models.CASCADE, related_name='variantes')
    color = models.CharField(max_length=50)
    talla = models.CharField(max_length=20)
    cantidad = models.PositiveIntegerField(default=1)
    estatus = models.CharField(max_length=20, choices=Prenda.ESTATUS, default='disponible')
    imagen = models.ImageField(upload_to='variantes/', null=True, blank=True)

    class Meta:
        unique_together = ('prenda', 'color', 'talla')

    def __str__(self):
        return f"{self.prenda.nombre} - {self.color} - {self.talla}"