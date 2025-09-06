from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_rentas, name='lista_rentas'),
    path('nueva/', views.nueva_renta, name='nueva_renta'),
    path('finalizar/<int:pk>/', views.finalizar_renta, name='finalizar_renta'),
    path('clientes/', views.lista_clientes, name='lista_clientes'),
    path('clientes/nuevo/', views.nuevo_cliente, name='nuevo_cliente'),
]