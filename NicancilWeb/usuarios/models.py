# Modelos de Usuarios
from django.contrib.auth.models import AbstractUser
from django.db import models

# Seleccion de Usuarios
class Usuario(AbstractUser):
    ROLES=(
        ("admin", "Administrador"),
        ("emp", "Empleado"),
        )
    rol=models.CharField(max_length=10, choices=ROLES, default="emp")
    telefono = models.CharField(max_length=15, blank=True, null=True)
    foto_perfil = models.ImageField(upload_to='perfiles/', blank=True, null=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}" if self.first_name else self.username
