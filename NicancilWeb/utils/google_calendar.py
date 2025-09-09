import os
import json
from django.conf import settings
from google.oauth2 import service_account
from googleapiclient.discovery import build

def get_google_calendar_credentials():
    """
    Obtiene las credenciales de Google Calendar desde variables de entorno
    """
    credentials_dict = {
        "type": os.getenv('GOOGLE_CALENDAR_TYPE'),
        "project_id": os.getenv('GOOGLE_CALENDAR_PROJECT_ID'),
        "private_key_id": os.getenv('GOOGLE_CALENDAR_PRIVATE_KEY_ID'),
        "private_key": os.getenv('GOOGLE_CALENDAR_PRIVATE_KEY').replace('\\n', '\n'),
        "client_email": os.getenv('GOOGLE_CALENDAR_CLIENT_EMAIL'),
        "client_id": os.getenv('GOOGLE_CALENDAR_CLIENT_ID'),
        "auth_uri": os.getenv('GOOGLE_CALENDAR_AUTH_URI'),
        "token_uri": os.getenv('GOOGLE_CALENDAR_TOKEN_URI'),
        "auth_provider_x509_cert_url": os.getenv('GOOGLE_CALENDAR_AUTH_PROVIDER_X509_CERT_URL'),
        "client_x509_cert_url": os.getenv('GOOGLE_CALENDAR_CLIENT_X509_CERT_URL'),
        "universe_domain": os.getenv('GOOGLE_CALENDAR_UNIVERSE_DOMAIN')
    }
    
    credentials = service_account.Credentials.from_service_account_info(
        credentials_dict,
        scopes=['https://www.googleapis.com/auth/calendar']
    )
    
    return credentials

def get_calendar_service():
    """
    Obtiene el servicio de Google Calendar
    """
    credentials = get_google_calendar_credentials()
    service = build('calendar', 'v3', credentials=credentials)
    return service