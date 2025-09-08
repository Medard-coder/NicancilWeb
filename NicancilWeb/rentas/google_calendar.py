from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from django.conf import settings
import datetime
import os

class GoogleCalendarService:
    def __init__(self):
        self.service = build('calendar', 'v3', credentials=self._get_credentials())
    
    def _get_credentials(self):
        # Ruta al archivo de credenciales
        credentials_path = os.path.join(settings.BASE_DIR, 'credentials', 'google_calendar_credentials.json')
        return Credentials.from_service_account_file(
            credentials_path,
            scopes=['https://www.googleapis.com/auth/calendar']
        )
    
    def crear_evento_renta(self, prenda, renta):
        evento = {
            'summary': f'Renta - {prenda.variante.prenda.nombre}',
            'description': f'Cliente: {renta.cliente.nombre}\nPrenda: {prenda}',
            'start': {
                'dateTime': renta.fecha_inicio.isoformat(),
                'timeZone': 'America/Mexico_City',
            },
            'end': {
                'dateTime': renta.fecha_fin.isoformat(),
                'timeZone': 'America/Mexico_City',
            },
        }
        
        return self.service.events().insert(
            calendarId=settings.GOOGLE_CALENDAR_ID,
            body=evento
        ).execute()
    
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