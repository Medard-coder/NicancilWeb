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
    return render(request, 'inventario/inventario.html', {'prendas': prendas})
