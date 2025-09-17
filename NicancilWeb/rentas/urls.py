from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_rentas, name='lista_rentas'),
    path('nueva/', views.nueva_renta, name='nueva_renta'),
    path('clientes/', views.lista_clientes, name='lista_clientes'),

    path('api/prenda/<int:prenda_id>/calendario/', views.calendario_prenda, name='calendario_prenda'),
    path('api/prenda/<int:prenda_id>/disponibilidad/', views.disponibilidad_prenda, name='disponibilidad_prenda'),
    path('api/renta/<int:renta_id>/sincronizar/', views.sincronizar_google_calendar, name='sincronizar_google_calendar'),
    path('api/renta/<int:renta_id>/finalizar/', views.finalizar_renta_api, name='finalizar_renta_api'),
]