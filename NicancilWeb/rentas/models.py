from django.db import models
from django.core.exceptions import ValidationError
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
    
    def rentas_activas(self):
        return self.rentas.filter(estado='activa').count()

class Renta(models.Model):
    ESTADOS = (
        ('activa', 'Activa'),
        ('pendiente_devolucion', 'Pendiente de Devolución'),
        ('finalizada', 'Finalizada'),
    )
    
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='rentas')
    prendas = models.ManyToManyField(PrendaUnidad, related_name='rentas')
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    precio_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='activa')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Renta"
        verbose_name_plural = "Rentas"
        ordering = ['-fecha_creacion']
    
    def clean(self):
        if self.fecha_fin <= self.fecha_inicio:
            raise ValidationError('La fecha de fin debe ser posterior a la fecha de inicio')
    
    def validar_prendas_disponibles(self):
        prendas_no_disponibles = self.prendas.exclude(estatus='disponible')
        if prendas_no_disponibles.exists():
            nombres = [str(p) for p in prendas_no_disponibles]
            raise ValidationError(f'Las siguientes prendas no están disponibles: {", ".join(nombres)}')
    
    def calcular_precio_total(self):
        total = sum(prenda.variante.prenda.precio for prenda in self.prendas.all())
        self.precio_total = total
        return total
    
    def finalizar_renta(self):
        self.estado = 'finalizada'
        for prenda in self.prendas.all():
            prenda.estatus = 'disponible'
            prenda.save()
        self.save()
    
    def __str__(self):
        return f"Renta {self.id} - {self.cliente.nombre}"

# Señales para gestionar estatus de prendas
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver

@receiver(m2m_changed, sender=Renta.prendas.through)
def cambiar_estatus_prendas(sender, instance, action, pk_set, **kwargs):
    if action == 'pre_add' and instance.estado == 'activa':
        # Validar que las prendas estén disponibles antes de agregarlas
        prendas_no_disponibles = PrendaUnidad.objects.filter(pk__in=pk_set).exclude(estatus='disponible')
        if prendas_no_disponibles.exists():
            nombres = [str(p) for p in prendas_no_disponibles]
            raise ValidationError(f'Las siguientes prendas no están disponibles: {", ".join(nombres)}')
    elif action == 'post_add' and instance.estado == 'activa':
        # Cambiar prendas a 'en_uso' cuando se agregan a una renta activa
        PrendaUnidad.objects.filter(pk__in=pk_set).update(estatus='en_uso')
    elif action == 'post_remove':
        # Cambiar prendas a 'disponible' cuando se quitan de una renta
        PrendaUnidad.objects.filter(pk__in=pk_set).update(estatus='disponible')