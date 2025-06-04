from django.shortcuts import render

def index(request):
    return render(request, 'catalogo/index.html')

def inventario(request):
    return render(request, 'catalogo/inventario.html')

def citas(request):
    return render(request, 'catalogo/citas.html')

def rentas(request):
    return render(request, 'catalogo/rentas.html')

def lavado(request):
    return render(request, 'catalogo/lavado.html')

def reportes(request):
    return render(request, 'catalogo/reportes.html')

def agregar(request):
    return render(request, 'catalogo/agregar.html')
