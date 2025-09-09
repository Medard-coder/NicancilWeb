from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, render
from inventario.models import PrendaUnidad
from .models import Renta, Cliente
import json
from datetime import datetime, timedelta

def lista_prendas_calendario(request):
    """Vista para mostrar todas las prendas con sus calendarios"""
    prendas = PrendaUnidad.objects.all()
    return render(request, 'rentas/lista_prendas_calendario.html', {'prendas': prendas})

def lista_rentas(request):
    """Vista para listar todas las rentas"""
    rentas = Renta.objects.all().order_by('-fecha_creacion')
    
    # Obtener rentas activas para el calendario
    rentas_activas = Renta.objects.filter(estado='activa')
    eventos_calendario = []
    
    for renta in rentas_activas:
        eventos_calendario.append({
            'title': f"Renta #{renta.id} - {renta.cliente.nombre}",
            'start': renta.fecha_inicio.strftime('%Y-%m-%d'),
            'end': renta.fecha_fin.strftime('%Y-%m-%d'),
            'color': '#007bff',
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
        # Lógica para crear renta
        pass
    
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