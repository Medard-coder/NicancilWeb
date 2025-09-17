# Configuración de Google Calendar

## Pasos para configurar Google Calendar:

### 1. Crear proyecto en Google Cloud Console
1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Crea un nuevo proyecto o selecciona uno existente
3. Habilita la API de Google Calendar

### 2. Crear credenciales de cuenta de servicio
1. Ve a "APIs y servicios" > "Credenciales"
2. Clic en "Crear credenciales" > "Cuenta de servicio"
3. Completa el formulario y crea la cuenta
4. Descarga el archivo JSON de credenciales

### 3. Configurar el proyecto Django
1. Crea la carpeta `credentials` en la raíz del proyecto
2. Guarda el archivo JSON como `google_calendar_credentials.json`
3. Agrega las siguientes variables al archivo `.env`:

```
GOOGLE_CALENDAR_ID=tu_calendar_id@gmail.com
```

### 4. Compartir el calendario
1. Ve a Google Calendar
2. Comparte tu calendario con la cuenta de servicio (email de la cuenta de servicio)
3. Dale permisos de "Hacer cambios en los eventos"

### 5. Instalar dependencias
```bash
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

## Estructura de archivos:
```
NicancilWeb/
├── credentials/
│   └── google_calendar_credentials.json
├── .env
└── ...
```

## Variables de entorno necesarias:
- `GOOGLE_CALENDAR_ID`: ID del calendario de Google