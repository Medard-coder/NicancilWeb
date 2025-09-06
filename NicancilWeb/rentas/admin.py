from django.contrib import admin
from .models import Renta, Cliente

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'telefono', 'correo', 'fecha_registro')
    search_fields = ('nombre', 'telefono', 'correo')
    list_filter = ('fecha_registro',)
    ordering = ('nombre',)

@admin.register(Renta)
class RentaAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'precio_total', 'estado', 'fecha_inicio', 'fecha_fin')
    list_filter = ('estado', 'fecha_inicio')
    search_fields = ('cliente__nombre',)
    filter_horizontal = ('prendas',)