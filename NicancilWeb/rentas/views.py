from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Renta, Cliente
from inventario.models import PrendaUnidad
from .forms import RentaForm, ClienteForm

@login_required
def lista_rentas(request):
    rentas = Renta.objects.all()
    return render(request, 'rentas/lista_rentas.html', {'rentas': rentas})

@login_required
def nueva_renta(request):
    if request.method == 'POST':
        form = RentaForm(request.POST)
        prendas_ids = request.POST.getlist('prendas')
        
        if form.is_valid() and prendas_ids:
            renta = form.save(commit=False)
            renta.precio_total = 0
            renta.save()
            
            # Agregar prendas seleccionadas
            prendas = PrendaUnidad.objects.filter(id__in=prendas_ids, estatus='disponible')
            renta.prendas.set(prendas)
            
            # Calcular precio total
            renta.calcular_precio_total()
            renta.save()
            
            messages.success(request, 'Renta creada exitosamente.')
            return redirect('lista_rentas')
        elif not prendas_ids:
            messages.error(request, 'Debe seleccionar al menos una prenda.')
    else:
        form = RentaForm()
    
    prendas_disponibles = PrendaUnidad.objects.filter(estatus='disponible')
    
    return render(request, 'rentas/nueva_renta.html', {
        'form': form,
        'prendas_disponibles': prendas_disponibles
    })

@login_required
def finalizar_renta(request, pk):
    renta = get_object_or_404(Renta, pk=pk)
    if request.method == 'POST':
        renta.finalizar_renta()
        messages.success(request, 'Renta finalizada exitosamente.')
        return redirect('lista_rentas')
    return render(request, 'rentas/confirmar_finalizar.html', {'renta': renta})

@login_required
def lista_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'rentas/lista_clientes.html', {'clientes': clientes})

@login_required
def nuevo_cliente(request):
    redirect_to = request.GET.get('next', 'lista_clientes')
    
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save()
            messages.success(request, f'Cliente "{cliente.nombre}" creado exitosamente.')
            
            # Si viene desde nueva_renta, redirigir allá
            if redirect_to == 'nueva_renta':
                return redirect('nueva_renta')
            else:
                return redirect('lista_clientes')
    else:
        form = ClienteForm()
    
    context = {
        'form': form,
        'redirect_to': redirect_to
    }
    return render(request, 'rentas/nuevo_cliente.html', context)

@login_required
def editar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, f'Cliente "{cliente.nombre}" editado exitosamente.')
            return redirect('lista_clientes')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'rentas/editar_cliente.html', {'form': form, 'cliente': cliente})

@login_required
def eliminar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.delete()
        messages.success(request, f'Cliente "{cliente.nombre}" eliminado exitosamente.')
        return redirect('lista_clientes')
    return render(request, 'rentas/confirmar_eliminar_cliente.html', {'cliente': cliente})