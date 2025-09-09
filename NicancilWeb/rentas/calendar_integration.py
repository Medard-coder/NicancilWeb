from utils.google_calendar import get_calendar_service
from datetime import datetime

def crear_evento_renta(renta):
    """
    Crea un evento en Google Calendar para una renta
    """
    service = get_calendar_service()
    
    evento = {
        'summary': f'Renta - {renta.cliente.nombre}',
        'description': f'Renta de prendas para {renta.cliente.nombre}\nTeléfono: {renta.cliente.telefono}',
        'start': {
            'dateTime': renta.fecha_inicio.isoformat(),
            'timeZone': 'America/Mexico_City',
        },
        'end': {
            'dateTime': renta.fecha_fin.isoformat(),
            'timeZone': 'America/Mexico_City',
        },
        'attendees': [
            {'email': renta.cliente.correo},
        ],
    }
    
    evento_creado = service.events().insert(calendarId='primary', body=evento).execute()
    return evento_creado.get('id')

def actualizar_evento_renta(evento_id, renta):
    """
    Actualiza un evento existente en Google Calendar
    """
    service = get_calendar_service()
    
    evento = service.events().get(calendarId='primary', eventId=evento_id).execute()
    
    evento['summary'] = f'Renta - {renta.cliente.nombre}'
    evento['description'] = f'Renta de prendas para {renta.cliente.nombre}\nTeléfono: {renta.cliente.telefono}'
    evento['start']['dateTime'] = renta.fecha_inicio.isoformat()
    evento['end']['dateTime'] = renta.fecha_fin.isoformat()
    
    evento_actualizado = service.events().update(calendarId='primary', eventId=evento_id, body=evento).execute()
    return evento_actualizado

def eliminar_evento_renta(evento_id):
    """
    Elimina un evento de Google Calendar
    """
    service = get_calendar_service()
    service.events().delete(calendarId='primary', eventId=evento_id).execute()