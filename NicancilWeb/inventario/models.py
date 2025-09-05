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
    estatus = models.CharField(max_length=20, choices=Prenda.ESTATUS)
    imagen = models.ImageField(upload_to='variantes/', null=True, blank=True)

    class Meta:
        unique_together = ('prenda', 'color', 'talla')

    def __str__(self):
        return f"{self.prenda.nombre} - {self.color} - {self.talla}"
    
    def unidades_disponibles(self):
        return self.unidades.filter(estatus='disponible').count()
    
    def total_unidades(self):
        return self.unidades.count()
    
class PrendaUnidad(models.Model):
    variante=models.ForeignKey(PrendaVariante, on_delete=models.CASCADE, related_name='unidades' )
    numero_serie=models.CharField(max_length=20, unique=True)
    estatus=models.CharField(max_length=20, choices=Prenda.ESTATUS, default='disponible')
    fecha_creacion=models.DateTimeField(auto_now_add=True)
    notas=models.TextField(blank=True, help_text="Notas adicionales sobre la unidad")
    
    class Meta:
        verbose_name="Unidad de Prenda"
        verbose_name_plural="Unidades de Prenda"
        ordering=['numero_serie']
    
    def __str__(self):
        return f"{self.variante} #{self.numero_serie}"
    
    def save(self, *args, **kwargs):
        if not self.numero_serie:
            #Generar numero de serie con estructura: NOM-TAL-COL-NUM
            nombre_prefix = self.variante.prenda.nombre[:3].upper().replace(' ', '')
            talla_prefix = self.variante.talla[:3].upper().replace(' ', '')
            color_prefix = self.variante.color[:3].upper().replace(' ', '')
            count = PrendaUnidad.objects.filter(variante=self.variante).count()
            self.numero_serie = f"{nombre_prefix}-{talla_prefix}-{color_prefix}-{count+1:03d}"
        super().save(*args, **kwargs)
        
def crear_unidades_automaticamente(sender, instantce, created, **kwargs):
    if created:
        #Crear unidades para cada variante automaticamente
        for i in range(instance.cantidad):
            PrimeraUnidad.objects.create(variante=instance)
            
#Conectar la señal
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=PrendaVariante)
def crear_unidades_automaticamente(sender, instance, created, **kwargs):
    if created:
        #Crear unidades para cada variante automaticamente
        for i in range(instance.cantidad):
            PrendaUnidad.objects.create(variante=instance, estatus=instance.estatus)

@receiver(post_save, sender=Prenda)
def crear_variante_original(sender, instance, created, **kwargs):
    if created:
        #Crear variante original automáticamente
        variante_original = PrendaVariante.objects.create(
            prenda=instance,
            color=instance.color or 'Original',
            talla=instance.tallas or 'Única',
            cantidad=instance.cantidad,
            estatus=instance.estatus
        )

