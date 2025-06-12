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
