from django.contrib import admin
from .models import Prenda, PrendaVariante, PrendaUnidad

@admin.register(Prenda)
class PrendaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'tipo', 'descripcion', 'imagen')
    search_fields = ('nombre', 'tipo')
    list_filter = ('tipo', )
    
class PrendaUnidadInline(admin.TabularInline):
    model = PrendaUnidad
    extra = 1
    fields = ['numero_serie', 'estatus', 'notas']

@admin.register(PrendaVariante)
class PrendaVarianteAdmin(admin.ModelAdmin):
    list_display = ('prenda', 'color', 'talla', 'cantidad', 'estatus')
    search_fields = ('prenda__nombre', 'color', 'talla')
    list_filter = ('estatus', 'color')
    
@admin.register(PrendaUnidad)
class PrendaUnidadAdmin(admin.ModelAdmin):
    list_display=('numero_serie', 'variante', 'estatus', 'fecha_creacion')
    list_filter = ('estatus',)
    search_fields=('numero_serie',)
