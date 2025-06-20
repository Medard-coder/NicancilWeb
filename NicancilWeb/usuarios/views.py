# Vistas de Usuarios
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoginForm, RegistroForm

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
    # Obtener todas las prendas para mostrarlas en el dashboard
    from inventario.models import Prenda
    prendas = Prenda.objects.all()
    
    if request.user.rol == 'admin':
        return render(request, "usuarios/dashboard_admin.html", {'prendas': prendas})
    elif request.user.rol == 'emp':
        return render(request, "usuarios/dashboard_empleado.html", {'prendas': prendas})
    else:
        return redirect('logout')

# Vista para registro de usuarios empleados
def registro_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.rol = 'emp'  # Solo crear usuarios empleados
            usuario.save()
            messages.success(request, 'Usuario empleado creado exitosamente.')
            return redirect('login')
    else:
        form = RegistroForm()
    
    return render(request, 'usuarios/registro.html', {'form': form})
