from django.contrib import admin
from .models import Cita

@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ['id', 'cliente', 'fecha_cita', 'estado', 'fecha_registro']
    list_filter = ['estado', 'fecha_cita', 'fecha_registro']
    search_fields = ['cliente__nombre', 'motivo']
    ordering = ['-fecha_cita']