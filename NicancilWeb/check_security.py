#!/usr/bin/env python
"""
Script de verificación de configuración de seguridad
Ejecutar: python check_security.py
"""
import os
import sys
from pathlib import Path

# Agregar el directorio del proyecto al path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NicancilWeb.settings')
import django
django.setup()

from django.conf import settings
from django.core.management import call_command

def check_security():
    """Verificar configuración de seguridad"""
    print("=" * 60)
    print("VERIFICACIÓN DE SEGURIDAD - NicancilWeb")
    print("=" * 60)
    print()
    
    issues = []
    warnings = []
    success = []
    
    # 1. Verificar SECRET_KEY
    print("1. Verificando SECRET_KEY...")
    if os.environ.get('DJANGO_SECRET_KEY'):
        success.append("[OK] SECRET_KEY configurada en variable de entorno")
    else:
        warnings.append("[!] SECRET_KEY no esta en variable de entorno (usando temporal)")
    
    # 2. Verificar DEBUG
    print("2. Verificando DEBUG...")
    if settings.DEBUG:
        warnings.append("[!] DEBUG=True (desactivar en produccion)")
    else:
        success.append("[OK] DEBUG=False")
    
    # 3. Verificar ALLOWED_HOSTS
    print("3. Verificando ALLOWED_HOSTS...")
    if settings.ALLOWED_HOSTS == ['localhost', '127.0.0.1']:
        warnings.append("[!] ALLOWED_HOSTS solo tiene localhost (configurar para produccion)")
    else:
        success.append(f"[OK] ALLOWED_HOSTS configurado: {settings.ALLOWED_HOSTS}")
    
    # 4. Verificar HTTPS
    print("4. Verificando configuracion HTTPS...")
    if settings.SECURE_SSL_REDIRECT:
        success.append("[OK] SECURE_SSL_REDIRECT activado")
    else:
        warnings.append("[!] SECURE_SSL_REDIRECT desactivado (activar en produccion)")
    
    # 5. Verificar CORS
    print("5. Verificando CORS...")
    if 'corsheaders' in settings.INSTALLED_APPS:
        success.append("[OK] django-cors-headers instalado")
    else:
        issues.append("[X] django-cors-headers no esta en INSTALLED_APPS")
    
    # 6. Verificar Rate Limiting
    print("6. Verificando Rate Limiting...")
    if 'NicancilWeb.middleware.RateLimitMiddleware' in settings.MIDDLEWARE:
        success.append("[OK] Rate Limiting middleware configurado")
    else:
        issues.append("[X] Rate Limiting middleware no configurado")
    
    # 7. Verificar Cache
    print("7. Verificando Cache...")
    if settings.CACHES:
        success.append("[OK] Cache configurado")
    else:
        warnings.append("[!] Cache no configurado")
    
    # 8. Verificar Logging
    print("8. Verificando Logging...")
    if settings.LOGGING:
        success.append("[OK] Logging configurado")
        # Verificar que el directorio logs existe
        logs_dir = BASE_DIR / 'logs'
        if logs_dir.exists():
            success.append("[OK] Directorio logs existe")
        else:
            warnings.append("[!] Directorio logs no existe")
    else:
        warnings.append("[!] Logging no configurado")
    
    # 9. Verificar archivo .env
    print("9. Verificando archivo .env...")
    env_file = BASE_DIR / '.env'
    if env_file.exists():
        success.append("[OK] Archivo .env existe")
    else:
        warnings.append("[!] Archivo .env no existe (copiar de .env.example)")
    
    # 10. Ejecutar checks de Django
    print("10. Ejecutando checks de Django...")
    print()
    try:
        call_command('check', '--deploy')
        success.append("[OK] Django checks pasados")
    except Exception as e:
        issues.append(f"[X] Django checks fallaron: {str(e)}")
    
    # Resumen
    print()
    print("=" * 60)
    print("RESUMEN")
    print("=" * 60)
    print()
    
    if success:
        print("[OK] CONFIGURACIONES CORRECTAS:")
        for item in success:
            print(f"   {item}")
        print()
    
    if warnings:
        print("[!] ADVERTENCIAS:")
        for item in warnings:
            print(f"   {item}")
        print()
    
    if issues:
        print("[X] PROBLEMAS CRITICOS:")
        for item in issues:
            print(f"   {item}")
        print()
    
    # Puntuación
    total = len(success) + len(warnings) + len(issues)
    score = (len(success) / total * 100) if total > 0 else 0
    
    print("=" * 60)
    print(f"PUNTUACIÓN DE SEGURIDAD: {score:.1f}%")
    print("=" * 60)
    print()
    
    if score >= 80:
        print("[OK] Excelente! Tu configuracion de seguridad es solida.")
    elif score >= 60:
        print("[OK] Buena configuracion, pero hay areas de mejora.")
    else:
        print("[!] Se requiere atencion urgente a la seguridad.")
    
    print()
    print("Para más información, consulta SECURITY_SETUP.md")
    print()

if __name__ == '__main__':
    check_security()
