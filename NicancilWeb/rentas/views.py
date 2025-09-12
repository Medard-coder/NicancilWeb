from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from inventario.models import PrendaUnidad
from .models import Renta, Cliente
from .forms import RentaForm, ClienteForm
import json
from datetime import datetime, timedelta

def lista_prendas_calendario(request):
    """Vista para mostrar todas las prendas con sus calendarios"""
    prendas = PrendaUnidad.objects.all()
    return render(request, 'rentas/lista_prendas_calendario.html', {'prendas': prendas})

def lista_rentas(request):
    """Vista para listar todas las rentas"""
    from django.utils import timezone
    
    # Actualizar rentas vencidas automáticamente
    rentas_vencidas = Renta.objects.filter(
        estado='activa',
        fecha_fin__lt=timezone.now()
    )
    rentas_vencidas.update(estado='pendiente_devolucion')
    
    rentas = Renta.objects.all().order_by('-fecha_creacion')
    
    # Obtener rentas activas y pendientes para el calendario
    rentas_calendario = Renta.objects.filter(estado__in=['activa', 'pendiente_devolucion'])
    eventos_calendario = []
    
    for renta in rentas_calendario:
        color = '#007bff' if renta.estado == 'activa' else '#dc3545'
        eventos_calendario.append({
            'title': f"Renta #{renta.id} - {renta.cliente.nombre}",
            'start': renta.fecha_inicio.strftime('%Y-%m-%d'),
            'end': renta.fecha_fin.strftime('%Y-%m-%d'),
            'color': color,
            'textColor': '#fff'
        })
    
    return render(request, 'rentas/lista_rentas.html', {
        'rentas': rentas,
        'eventos_calendario': json.dumps(eventos_calendario)
    })

def lista_clientes(request):
    """Vista para listar todos los clientes"""
    clientes = Cliente.objects.all().order_by('nombre')
    return render(request, 'rentas/lista_clientes.html', {'clientes': clientes})

def nueva_renta(request):
    """Vista para crear nueva renta"""
    if request.method == 'POST':
        cliente_id = request.POST.get('cliente')
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')
        prendas_ids = request.POST.getlist('prendas')
        
        if cliente_id and fecha_inicio and fecha_fin and prendas_ids:
            try:
                cliente = Cliente.objects.get(id=cliente_id)
                
                # Crear la renta
                renta = Renta.objects.create(
                    cliente=cliente,
                    fecha_inicio=datetime.fromisoformat(fecha_inicio),
                    fecha_fin=datetime.fromisoformat(fecha_fin),
                    precio_total=0
                )
                
                # Agregar prendas y calcular precio
                prendas = PrendaUnidad.objects.filter(id__in=prendas_ids, estatus='disponible')
                renta.prendas.set(prendas)
                renta.calcular_precio_total()
                renta.save()
                
                messages.success(request, f'Renta #{renta.id} creada exitosamente.')
                return redirect('lista_rentas')
                
            except Exception as e:
                messages.error(request, f'Error al crear la renta: {str(e)}')
        else:
            messages.error(request, 'Todos los campos son obligatorios.')
    
    clientes = Cliente.objects.all()
    prendas = PrendaUnidad.objects.filter(estatus='disponible')
    return render(request, 'rentas/nueva_renta.html', {
        'clientes': clientes,
        'prendas': prendas
    })

def sincronizar_google_calendar(request, renta_id):
    """Sincronizar renta con Google Calendar"""
    from .google_calendar import GoogleCalendarService
    
    renta = get_object_or_404(Renta, id=renta_id)
    calendar_service = GoogleCalendarService()
    
    try:
        for prenda in renta.prendas.all():
            calendar_service.crear_evento_renta(prenda, renta)
        
        return JsonResponse({'success': True, 'message': 'Eventos creados en Google Calendar'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@csrf_exempt
def calendario_prenda(request, prenda_id):
    """API para obtener fechas ocupadas de una prenda específica"""
    prenda = get_object_or_404(PrendaUnidad, id=prenda_id)
    
    # Obtener rentas activas de esta prenda
    rentas = Renta.objects.filter(
        prendas=prenda,
        estado='activa'
    ).values('fecha_inicio', 'fecha_fin', 'cliente__nombre')
    
    eventos = []
    for renta in rentas:
        eventos.append({
            'title': f"Rentado - {renta['cliente__nombre']}",
            'start': renta['fecha_inicio'].strftime('%Y-%m-%d'),
            'end': renta['fecha_fin'].strftime('%Y-%m-%d'),
            'color': '#dc3545',
            'textColor': '#fff'
        })
    
    return JsonResponse(eventos, safe=False)

@csrf_exempt
def disponibilidad_prenda(request, prenda_id):
    """Verificar disponibilidad de prenda en fechas específicas"""
    if request.method == 'POST':
        data = json.loads(request.body)
        fecha_inicio = datetime.strptime(data['fecha_inicio'], '%Y-%m-%d')
        fecha_fin = datetime.strptime(data['fecha_fin'], '%Y-%m-%d')
        
        conflictos = Renta.objects.filter(
            prendas__id=prenda_id,
            estado='activa',
            fecha_inicio__lt=fecha_fin,
            fecha_fin__gt=fecha_inicio
        ).exists()
        
        return JsonResponse({
            'disponible': not conflictos,
            'mensaje': 'Disponible' if not conflictos else 'No disponible en esas fechas'
        })

def finalizar_renta(request, pk):
    renta = get_object_or_404(Renta, pk=pk)
    if request.method == 'POST':
        renta.finalizar_renta()
        messages.success(request, 'Renta finalizada exitosamente.')
        return redirect('lista_rentas')
    return render(request, 'rentas/confirmar_finalizar.html', {'renta': renta})

def nuevo_cliente(request):
    redirect_to = request.GET.get('next', 'lista_clientes')
    
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save()
            messages.success(request, f'Cliente "{cliente.nombre}" creado exitosamente.')
            
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

def eliminar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.delete()
        messages.success(request, f'Cliente "{cliente.nombre}" eliminado exitosamente.')
        return redirect('lista_clientes')
    return render(request, 'rentas/confirmar_eliminar_cliente.html', {'cliente': cliente})