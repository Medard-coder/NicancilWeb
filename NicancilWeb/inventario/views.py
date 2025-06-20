from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Prenda
from .forms import PrendaForm

# Vista para listar prendas
def prenda_lista(request):
    prendas = Prenda.objects.all()
    return render(request, 'inventario/prenda_lista.html', {'prendas': prendas})

# Vista para ver detalle de una prenda
def prenda_detalle(request, pk):
    prenda = get_object_or_404(Prenda, pk=pk)
    return render(request, 'inventario/prenda_detalle.html', {'prenda': prenda})

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
            prenda=form.save()
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

#Vista para ver el inventario (administradores y empleados)
@login_required
def inventario(request):
    prendas = Prenda.objects.all()
    
    #Filtros de busqueda
    busqueda=request.GET.get('busqueda', '')
    tipo=request.GET.get('tipo', '')
    color=request.GET.get('color', '')
    genero=request.GET.get('genero', '')
    estatus=request.GET.get('estatus', '')
    talla=request.GET.get('talla', '')
    precio_min=request.GET.get('precio_min', '')
    precio_max=request.GET.get('precio_max', '')
    
    if busqueda:
        prendas=prendas.filter(nombre__icontains=busqueda)
    
    if tipo:
        prendas=prendas.filter(tipo=tipo)
        
    if color:
        prendas=prendas.filter(color=color)
        
    if genero:
        prendas=prendas.filter(genero=genero)
    
    if estatus:
        prendas=prendas.filter(estatus=estatus)
        
    if talla:
        prendas=prendas.filter(tallas__icontains=talla)
        
    if precio_min:
        try:
            prendas=prendas.filter(precio__gte=float(precio_min))
        except ValueError:
            pass
        
    if precio_max:
        try:
            prendas=prendas.filter(precio__lte=float(precio_max))
        except ValueError:
            pass
        
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
