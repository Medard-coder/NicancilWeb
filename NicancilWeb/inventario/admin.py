from django.contrib import admin
from .models import Prenda

@admin.register(Prenda)
class PrendaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'tipo', 'descripcion', 'imagen')
    search_fields = ('nombre', 'tipo')
    list_filter = ('tipo', )
