from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

# Register your models here
class UsuarioAdmin(UserAdmin):
    model=Usuario
    list_display = ["email", "is_staff", "is_superuser", "rol"]
    fieldsets=UserAdmin.fieldsets+(
        (None, {"fields": ("rol" ,)}),
    )
    
admin.site.register(Usuario, UsuarioAdmin)
