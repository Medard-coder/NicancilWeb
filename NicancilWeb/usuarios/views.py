# Vistas de Usuarios
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import LoginForm

# Vista para login
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    form = LoginForm(request, data=request.POST or None)
    if form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect("dashboard")
    
    return render(request, "usuarios/login.html", {"form": form})

# Vista para logout
def logout_view(request):
    logout(request)
    return redirect("login")

# Vista del Dashboard para redireccionar según el rol
@login_required
def dashboard(request):
    if request.user.rol == 'admin':
        return render(request, "usuarios/dashboard_admin.html")
    elif request.user.rol == 'emp':
        return render(request, "usuarios/dashboard_empleado.html")
    else:
        return redirect('logout')
