# Vistas de Usuarios
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import LoginForm

# Logica de los formularios
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    form=LoginForm(request, data=request.POST or None)
    if form.is_valid():
        user=form.get_user()
        login(request, user)
        return redirect("dashboard")
    return render(request, "usuarios/login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("login")

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect("login")
    
    if request.user.rol=='admin':
        return render(request, "usuarios/dashboard_admin.html")
    else:
        return render(request, "usuarios/dashboard_empleado.html")