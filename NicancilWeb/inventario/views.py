from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.html import escape
from django.db import IntegrityError
from .models import Prenda, PrendaVariante, PrendaUnidad
from .forms import PrendaForm, PrendaVarianteForm

# Vista para listar prendas
@login_required
def prenda_lista(request):
    prendas = Prenda.objects.all()
    return render(request, 'inventario/prenda_lista.html', {'prendas': prendas})

# Vista para ver detalle de una prenda
@login_required
def prenda_detalle(request, pk):
    prenda = get_object_or_404(Prenda, pk=pk)
    unidades=PrendaUnidad.objects.filter(variante__prenda=prenda)
    return render(request, 'inventario/prenda_detalle.html', {'prenda': prenda, 'unidades':unidades})

#Vista para crear una nueva prenda (solo Administradores)
@login_required
def nueva_prenda(request):
    if request.user.rol != 'admin':
        messages.error(request, 'No tienes permiso para agregar nuevas prendas.')
        return redirect('prenda_lista')
    
    if request.method == 'POST':
        form = PrendaForm(request.POST, request.FILES)
        if form.is_valid():
            prenda=form.save()
            messages.success(request, 'La prenda se ha agregado correctamente.')
            return redirect('prenda_detalle', pk=prenda.pk) 
    
    else:
        form=PrendaForm()
        
    return render(request, 'inventario/nueva_prenda.html', {'form': form})

#Vista para editar una prenda (Solo administradores)
@login_required
def editar_prenda(request, pk):
    if request.user.rol != 'admin':
        messages.error(request, 'No tienes permiso para editar prendas.')
        return redirect('prenda_lista')

    prenda = get_object_or_404(Prenda, pk=pk)

    if request.method == 'POST':
        form = PrendaForm(request.POST, request.FILES, instance=prenda)
        if form.is_valid():
            form.save()
            messages.success(request, 'La prenda se ha editado correctamente.')
            return redirect('prenda_lista')
    else:
        form = PrendaForm(instance=prenda)

    return render(request, 'inventario/editar_prenda.html', {'form': form, 'prenda': prenda})

#Vista para eliminar una prenda (Solo administradores)
@login_required
def eliminar_prenda(request, pk):
    if request.user.rol != 'admin':
        messages.error(request, 'No tienes permiso para eliminar prendas.')
        return redirect('prenda_lista')

    prenda = get_object_or_404(Prenda, pk=pk)
    if request.method == 'POST':
        prenda.delete()
        messages.success(request, 'La prenda se ha eliminado correctamente.')
        return redirect('prenda_lista')
    return render(request, 'inventario/confirmar_eliminar_prenda.html', {'prenda': prenda})

def _aplicar_filtros_basicos(prendas, filtros):
    """Aplica filtros básicos de texto a las prendas"""
    filtros_map = {
        'busqueda': 'nombre__icontains',
        'tipo': 'tipo',
        'color': 'color', 
        'genero': 'genero',
        'estatus': 'estatus',
        'talla': 'tallas__icontains'
    }
    
    for campo, valor in filtros.items():
        if valor and campo in filtros_map:
            prendas = prendas.filter(**{filtros_map[campo]: valor})
    return prendas

def _aplicar_filtro_precio(prendas, precio_str, operador):
    """Aplica filtro de precio con validación de NaN"""
    if not precio_str:
        return prendas
    
    try:
        precio_val = float(precio_str)
        if precio_val == precio_val:  # Check for NaN
            filtro = {f'precio__{operador}': precio_val}
            return prendas.filter(**filtro)
    except (ValueError, TypeError):
        pass
    return prendas

#Vista para ver el inventario (administradores y empleados) # cspell:ignore inventario
@login_required
def inventario(request):
    prendas = Prenda.objects.all()
    
    #Filtros de busqueda
    filtros = {
        'busqueda': escape(request.GET.get('busqueda', '').strip()),
        'tipo': escape(request.GET.get('tipo', '').strip()),
        'color': escape(request.GET.get('color', '').strip()),
        'genero': escape(request.GET.get('genero', '').strip()),
        'estatus': escape(request.GET.get('estatus', '').strip()),
        'talla': escape(request.GET.get('talla', '').strip())
    }
    
    prendas = _aplicar_filtros_basicos(prendas, filtros)
    prendas = _aplicar_filtro_precio(prendas, request.GET.get('precio_min', '').strip(), 'gte')
    prendas = _aplicar_filtro_precio(prendas, request.GET.get('precio_max', '').strip(), 'lte')
        
    #Obtener opciones de filtros
    tipos_prenda=Prenda.TIPOS
    colores=Prenda.objects.values_list('color', flat=True).distinct()
    generos=Prenda.GENEROS
    estatus_opciones=Prenda.ESTATUS
    
    context={
        'prendas': prendas,
        'tipos_prenda': tipos_prenda,
        'colores': colores,
        'generos': generos,
        'estatus_opciones': estatus_opciones,
        'tallas': Prenda.objects.values_list('tallas', flat=True).distinct(),
    }
    
    return render(request, 'inventario/inventario.html', context)

#Vista para gestionar variantes de una prenda
@login_required
def gestionar_variantes(request, pk):
    if request.user.rol != 'admin':
        messages.error(request, 'No tienes permiso para gestionar variantes.')
        return redirect('prenda_detalle', pk=pk)
    
    prenda = get_object_or_404(Prenda, pk=pk)
    
    if request.method == 'POST':
        form = PrendaVarianteForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                variante = form.save(commit=False)
                variante.prenda = prenda
                variante.save()
                messages.success(request, 'Variante agregada correctamente.')
                return redirect('gestionar_variantes', pk=pk)
            except IntegrityError:
                messages.error(request, 'Ya existe una variante con los mismos detalles.')
    else:
        form = PrendaVarianteForm()
    
    variantes = prenda.variantes.all()
    return render(request, 'inventario/gestionar_variantes.html', {
        'prenda': prenda,
        'variantes': variantes,
        'form': form
    })

#Vista para eliminar variante
@login_required
def eliminar_variante(request, pk):
    if request.user.rol != 'admin':
        messages.error(request, 'No tienes permiso para eliminar variantes.')
        return redirect('prenda_lista')
    
    variante = get_object_or_404(PrendaVariante, pk=pk)
    prenda_pk = variante.prenda.pk
    
    if request.method == 'POST':
        variante.delete()
        messages.success(request, 'Variante eliminada correctamente.')
        return redirect('gestionar_variantes', pk=prenda_pk)
    
    return render(request, 'inventario/confirmar_eliminar_variante.html', {'variante': variante})

#Vista para editar variante
@login_required
def editar_variante(request, pk):
    if request.user.rol != 'admin':
        messages.error(request, 'No tienes permiso para editar variantes.')
        return redirect('prenda_lista')

    variante = get_object_or_404(PrendaVariante, pk=pk)

    if request.method == 'POST':
        form = PrendaVarianteForm(request.POST, request.FILES, instance=variante)
        if form.is_valid():
            variante = form.save()
            messages.success(request, 'Variante editada correctamente.')
            return redirect('gestionar_variantes', pk=variante.prenda.pk)
    else:
        form = PrendaVarianteForm(instance=variante)

    return render(request, 'inventario/editar_variante.html', {'form': form, 'variante': variante})


