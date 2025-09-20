from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from inventario.models import PrendaUnidad, Prenda, PrendaVariante
from .models import Renta, Cliente
from .forms import ClienteForm
import json
from datetime import datetime

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
    """Vista para listar todos los clientes y manejar nuevo cliente"""
    from .forms import ClienteForm
    redirect_to = request.GET.get('next', 'lista_clientes')
    
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save()
            messages.success(request, f'Cliente "{cliente.nombre}" creado exitosamente.')
            
            if redirect_to == 'lista_citas':
                return redirect('lista_citas')
            else:
                return redirect('lista_clientes')
        else:
            # Mostrar errores de validación
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{error}')
    else:
        form = ClienteForm()
    
    clientes = Cliente.objects.all().order_by('nombre')
    return render(request, 'rentas/lista_clientes.html', {
        'clientes': clientes,
        'form': form,
        'redirect_to': redirect_to
    })

def nueva_renta(request):
    """Vista para crear nueva renta"""
    if request.method == 'POST':
        cliente_id = request.POST.get('cliente')
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')
        prendas_data = request.POST.get('prendas_data')
        
        if cliente_id and fecha_inicio and fecha_fin and prendas_data:
            try:
                cliente = Cliente.objects.get(id=cliente_id)
                prendas_seleccionadas = json.loads(prendas_data)
                
                # Crear la renta
                renta = Renta.objects.create(
                    cliente=cliente,
                    fecha_inicio=datetime.fromisoformat(fecha_inicio),
                    fecha_fin=datetime.fromisoformat(fecha_fin),
                    precio_total=0
                )
                
                # Agregar prendas seleccionadas
                prendas_unidades = []
                for item in prendas_seleccionadas:
                    unidades = PrendaUnidad.objects.filter(
                        variante_id=item['variante_id'],
                        estatus='disponible'
                    )[:item['cantidad']]
                    prendas_unidades.extend(unidades)
                
                renta.prendas.set(prendas_unidades)
                renta.calcular_precio_total()
                renta.save()
                
                # Sincronizar con Google Calendar
                try:
                    from .google_calendar import GoogleCalendarService
                    calendar_service = GoogleCalendarService()
                    evento = calendar_service.crear_evento_renta(renta)
                    messages.success(request, f'✅ Renta #{renta.id} creada y sincronizada exitosamente con Google Calendar.')
                except Exception as e:
                    messages.warning(request, f'⚠️ Renta #{renta.id} creada localmente, pero no se pudo sincronizar con Google Calendar: {str(e)}')
                
                return redirect('lista_rentas')
                
            except Exception as e:
                messages.error(request, f'Error al crear la renta: {str(e)}')
        else:
            messages.error(request, 'Todos los campos son obligatorios.')
    
    from inventario.models import Prenda
    clientes = Cliente.objects.all()
    prendas = Prenda.objects.filter(
        variantes__unidades__estatus='disponible'
    ).distinct().order_by('nombre')
    
    return render(request, 'rentas/nueva_renta.html', {
        'clientes': clientes,
        'prendas': prendas
    })

def sincronizar_google_calendar(request, renta_id):
    """Sincronizar renta con Google Calendar manualmente"""
    from .google_calendar import GoogleCalendarService
    
    renta = get_object_or_404(Renta, id=renta_id)
    
    try:
        calendar_service = GoogleCalendarService()
        # Usar actualizar_evento_renta que crea o actualiza según sea necesario
        evento = calendar_service.actualizar_evento_renta(renta)
        return JsonResponse({
            'success': True, 
            'message': f'Renta #{renta.id} sincronizada exitosamente con Google Calendar',
            'evento_id': evento.get('id')
        })
    except Exception as e:
        return JsonResponse({
            'success': False, 
            'message': f'Error al sincronizar: {str(e)}'
        })

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

@csrf_exempt
def finalizar_renta_api(request, renta_id):
    """API para finalizar/eliminar renta completamente"""
    if request.method == 'POST':
        renta = get_object_or_404(Renta, id=renta_id)
        
        try:
            # Liberar prendas antes de eliminar
            for prenda in renta.prendas.all():
                prenda.estatus = 'disponible'
                prenda.save()
            
            # Eliminar evento de Google Calendar
            try:
                from .google_calendar import GoogleCalendarService
                calendar_service = GoogleCalendarService()
                calendar_service.eliminar_evento_renta(renta)
            except Exception as e:
                pass  # Continuar aunque falle Google Calendar
            
            # Eliminar renta de la base de datos
            cliente_nombre = renta.cliente.nombre
            renta_id_temp = renta.id
            renta.delete()
            
            return JsonResponse({
                'success': True,
                'message': f'Renta #{renta_id_temp} del cliente {cliente_nombre} finalizada y eliminada exitosamente'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error al finalizar la renta: {str(e)}'
            })
    
    return JsonResponse({'success': False, 'message': 'Método no permitido'})

@csrf_exempt
def obtener_variantes_prenda(request, prenda_id):
    """API para obtener variantes y unidades disponibles de una prenda"""
    try:
        prenda = get_object_or_404(Prenda, id=prenda_id)
        variantes_data = []
        
        for variante in prenda.variantes.all():
            unidades_disponibles = variante.unidades.filter(estatus='disponible').count()
            if unidades_disponibles > 0:
                variantes_data.append({
                    'id': variante.id,
                    'color': variante.color,
                    'talla': variante.talla,
                    'unidades_disponibles': unidades_disponibles,
                    'imagen': variante.imagen.url if variante.imagen else None
                })
        
        return JsonResponse({
            'success': True,
            'prenda': {
                'id': prenda.id,
                'nombre': prenda.nombre,
                'precio': float(prenda.precio),
                'imagen': prenda.imagen.url if prenda.imagen else None
            },
            'variantes': variantes_data
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        })

def eliminar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        try:
            # Verificar que no tenga rentas activas
            if cliente.rentas_activas() > 0:
                return JsonResponse({
                    'success': False,
                    'message': 'No se puede eliminar: el cliente tiene rentas activas'
                })
            
            cliente_nombre = cliente.nombre
            cliente.delete()
            return JsonResponse({
                'success': True,
                'message': f'Cliente "{cliente_nombre}" eliminado exitosamente'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error al eliminar cliente: {str(e)}'
            })
    
    return JsonResponse({'success': False, 'message': 'Método no permitido'})