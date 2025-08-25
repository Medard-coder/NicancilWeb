from django.contrib import admin
from .models import Prenda, PrendaVariante

@admin.register(Prenda)
class PrendaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'tipo', 'descripcion', 'imagen')
    search_fields = ('nombre', 'tipo')
    list_filter = ('tipo', )

@admin.register(PrendaVariante)
class PrendaVarianteAdmin(admin.ModelAdmin):
    list_display = ('prenda', 'color', 'talla', 'cantidad', 'estatus')
    search_fields = ('prenda__nombre', 'color', 'talla')
    list_filter = ('estatus', 'color')
