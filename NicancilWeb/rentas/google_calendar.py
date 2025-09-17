from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from django.conf import settings
import datetime
import os

class GoogleCalendarService:
    def __init__(self):
        try:
            self.service = build('calendar', 'v3', credentials=self._get_credentials())
        except Exception as e:
            raise Exception(f'Error al conectar con Google Calendar: {str(e)}')
    
    def _get_credentials(self):
        # Ruta al archivo de credenciales
        credentials_path = os.path.join(settings.BASE_DIR, 'credentials', 'google_calendar_credentials.json')
        
        if not os.path.exists(credentials_path):
            raise Exception('Archivo de credenciales de Google Calendar no encontrado')
            
        return Credentials.from_service_account_file(
            credentials_path,
            scopes=['https://www.googleapis.com/auth/calendar']
        )
    
    def crear_evento_renta(self, renta):
        try:
            prendas_nombres = [str(p.variante.prenda.nombre) for p in renta.prendas.all()]
            prendas_str = ', '.join(prendas_nombres)
            
            evento = {
                'summary': f'Renta #{renta.id} - {renta.cliente.nombre}',
                'description': f'Cliente: {renta.cliente.nombre}\nPrendas: {prendas_str}\nTotal: ${renta.precio_total}\nEstado: {renta.get_estado_display()}',
                'start': {
                    'dateTime': renta.fecha_inicio.isoformat(),
                    'timeZone': 'America/Mexico_City',
                },
                'end': {
                    'dateTime': renta.fecha_fin.isoformat(),
                    'timeZone': 'America/Mexico_City',
                },
                'extendedProperties': {
                    'private': {
                        'renta_id': str(renta.id),
                        'estado': renta.estado
                    }
                }
            }
            
            return self.service.events().insert(
                calendarId=settings.GOOGLE_CALENDAR_ID,
                body=evento
            ).execute()
        except Exception as e:
            raise Exception(f'Error al crear evento en Google Calendar: {str(e)}')
    
    def actualizar_evento_renta(self, renta):
        try:
            # Buscar evento existente por renta_id
            eventos = self.service.events().list(
                calendarId=settings.GOOGLE_CALENDAR_ID,
                privateExtendedProperty=f'renta_id={renta.id}'
            ).execute()
            
            if eventos.get('items'):
                # Actualizar evento existente
                evento_id = eventos['items'][0]['id']
                prendas_nombres = [str(p.variante.prenda.nombre) for p in renta.prendas.all()]
                prendas_str = ', '.join(prendas_nombres)
                
                evento_actualizado = {
                    'summary': f'Renta #{renta.id} - {renta.cliente.nombre}',
                    'description': f'Cliente: {renta.cliente.nombre}\nPrendas: {prendas_str}\nTotal: ${renta.precio_total}\nEstado: {renta.get_estado_display()}',
                    'start': {
                        'dateTime': renta.fecha_inicio.isoformat(),
                        'timeZone': 'America/Mexico_City',
                    },
                    'end': {
                        'dateTime': renta.fecha_fin.isoformat(),
                        'timeZone': 'America/Mexico_City',
                    },
                    'extendedProperties': {
                        'private': {
                            'renta_id': str(renta.id),
                            'estado': renta.estado
                        }
                    }
                }
                
                return self.service.events().update(
                    calendarId=settings.GOOGLE_CALENDAR_ID,
                    eventId=evento_id,
                    body=evento_actualizado
                ).execute()
            else:
                # Crear nuevo evento si no existe
                return self.crear_evento_renta(renta)
        except Exception as e:
            raise Exception(f'Error al actualizar evento en Google Calendar: {str(e)}')
    
    def eliminar_evento_renta(self, renta):
        # Buscar evento existente por renta_id
        eventos = self.service.events().list(
            calendarId=settings.GOOGLE_CALENDAR_ID,
            privateExtendedProperty=f'renta_id={renta.id}'
        ).execute()
        
        if eventos.get('items'):
            evento_id = eventos['items'][0]['id']
            return self.service.events().delete(
                calendarId=settings.GOOGLE_CALENDAR_ID,
                eventId=evento_id
            ).execute()
        else:
            raise Exception('Evento no encontrado en Google Calendar')
    
    def obtener_eventos_prenda(self, prenda_id, fecha_inicio=None, fecha_fin=None):
        if not fecha_inicio:
            fecha_inicio = datetime.datetime.now()
        if not fecha_fin:
            fecha_fin = fecha_inicio + datetime.timedelta(days=90)
        
        eventos = self.service.events().list(
            calendarId=settings.GOOGLE_CALENDAR_ID,
            timeMin=fecha_inicio.isoformat() + 'Z',
            timeMax=fecha_fin.isoformat() + 'Z',
            q=f'prenda_id:{prenda_id}',
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        return eventos.get('items', [])