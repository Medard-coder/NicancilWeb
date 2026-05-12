"""
Middleware personalizado para rate limiting y seguridad adicional
"""
from django.core.cache import cache
from django.http import HttpResponseForbidden
from django.utils.deprecation import MiddlewareMixin
import time

class RateLimitMiddleware(MiddlewareMixin):
    """
    Middleware para limitar el número de peticiones por IP
    """
    def process_request(self, request):
        # Excluir rutas estáticas y admin
        if request.path.startswith('/static/') or request.path.startswith('/media/'):
            return None
        
        # Obtener IP del cliente
        ip = self.get_client_ip(request)
        
        # Configuración de rate limiting
        rate_limit = 100  # peticiones
        time_window = 60  # segundos (1 minuto)
        
        # Clave de cache para esta IP
        cache_key = f'rate_limit_{ip}'
        
        # Obtener contador actual
        request_count = cache.get(cache_key, 0)
        
        if request_count >= rate_limit:
            return HttpResponseForbidden(
                'Demasiadas peticiones. Por favor, intenta más tarde.'
            )
        
        # Incrementar contador
        cache.set(cache_key, request_count + 1, time_window)
        
        return None
    
    def get_client_ip(self, request):
        """Obtener IP real del cliente considerando proxies"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class SecurityHeadersMiddleware(MiddlewareMixin):
    """
    Middleware para agregar headers de seguridad adicionales
    """
    def process_response(self, request, response):
        # Content Security Policy
        response['Content-Security-Policy'] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval' "
            "https://cdn.jsdelivr.net https://cdnjs.cloudflare.com; "
            "style-src 'self' 'unsafe-inline' "
            "https://cdn.jsdelivr.net https://fonts.googleapis.com; "
            "font-src 'self' https://fonts.gstatic.com https://cdn.jsdelivr.net; "
            "img-src 'self' data: https:; "
        )
        
        # Referrer Policy
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # Permissions Policy
        response['Permissions-Policy'] = (
            'geolocation=(), microphone=(), camera=()'
        )
        
        return response
