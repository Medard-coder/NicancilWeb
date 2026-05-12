# Guía de Configuración de Seguridad - NicancilWeb

## Configuración Implementada

### 1. SECRET_KEY Segura
- **Problema**: La SECRET_KEY estaba expuesta en el código
- **Solución**: Ahora se carga desde variable de entorno
- **Acción requerida**: 
  ```bash
  # Genera una clave segura
  python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
  
  # Agrégala a tu archivo .env
  DJANGO_SECRET_KEY=tu-clave-generada-aqui
  ```

### 2. Configuración HTTPS
- **Headers de seguridad configurados**:
  - `SECURE_SSL_REDIRECT`: Redirige HTTP a HTTPS en producción
  - `SECURE_HSTS_SECONDS`: HTTP Strict Transport Security
  - `SESSION_COOKIE_SECURE`: Cookies solo por HTTPS
  - `CSRF_COOKIE_SECURE`: Protección CSRF por HTTPS
  - `SESSION_COOKIE_HTTPONLY`: Previene acceso JavaScript a cookies

- **Para activar en producción**:
  ```bash
  # En tu archivo .env
  SECURE_SSL_REDIRECT=True
  ```

### 3. CORS Configurado
- **Instalado**: django-cors-headers
- **Configuración**: 
  - Orígenes permitidos configurables por variable de entorno
  - Credenciales permitidas para autenticación
  
- **Personalizar**:
  ```bash
  # En .env
  CORS_ALLOWED_ORIGINS=https://tudominio.com,https://www.tudominio.com
  CSRF_TRUSTED_ORIGINS=https://tudominio.com,https://www.tudominio.com
  ```

### 4. Rate Limiting
- **Implementado**: Middleware personalizado
- **Límite**: 100 peticiones por minuto por IP
- **Excluye**: Archivos estáticos y media
- **Personalizable**: Edita `NicancilWeb/middleware.py`

### 5. Protección CSRF
- **Corregido**: Todas las vistas API ahora usan `@csrf_protect`
- **Vistas protegidas**:
  - calendario_prenda
  - disponibilidad_prenda
  - finalizar_renta_api
  - validar_extension_renta
  - extender_renta

### 6. Headers de Seguridad Adicionales
- **Content-Security-Policy**: Previene XSS
- **Referrer-Policy**: Controla información de referencia
- **Permissions-Policy**: Restringe APIs del navegador
- **X-Frame-Options**: Previene clickjacking
- **X-Content-Type-Options**: Previene MIME sniffing

### 7. Logging Configurado
- **Archivos de log**:
  - `logs/django.log`: Logs generales
  - `logs/security.log`: Logs de seguridad
- **Niveles**: WARNING y superior

## Pasos para Despliegue en Producción

### 1. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 2. Configurar Variables de Entorno
```bash
# Copia el archivo de ejemplo
cp .env.example .env

# Edita .env con tus valores reales
nano .env
```

### 3. Variables Críticas para Producción
```bash
DJANGO_SECRET_KEY=clave-super-segura-generada
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=tudominio.com,www.tudominio.com
SECURE_SSL_REDIRECT=True
CSRF_TRUSTED_ORIGINS=https://tudominio.com
CORS_ALLOWED_ORIGINS=https://tudominio.com
```

### 4. Configurar Servidor Web
- **Nginx/Apache**: Configurar SSL/TLS
- **Certificado**: Let's Encrypt (gratuito)
- **WSGI**: Gunicorn o uWSGI

### 5. Verificar Seguridad
```bash
# Ejecutar checks de Django
python manage.py check --deploy
```

## Mejoras Adicionales Recomendadas

### Corto Plazo
- [ ] Configurar backup automático de base de datos
- [ ] Implementar monitoreo de logs
- [ ] Configurar alertas de seguridad

### Mediano Plazo
- [ ] Migrar a PostgreSQL
- [ ] Implementar Redis para cache
- [ ] Configurar CDN para archivos estáticos

### Largo Plazo
- [ ] Implementar 2FA (autenticación de dos factores)
- [ ] Auditoría de seguridad profesional
- [ ] Penetration testing

## Recursos Útiles
- [Django Security Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Mozilla Observatory](https://observatory.mozilla.org/)

## Soporte
Para dudas sobre la configuración de seguridad, consulta la documentación oficial de Django o contacta al equipo de desarrollo.
