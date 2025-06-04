from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('inventario/', views.inventario, name='inventario'),
    path('citas/', views.citas, name='citas'),
    path('rentas/', views.rentas, name='rentas'),
    path('lavado/', views.lavado, name='lavado'),
    path('reportes/', views.reportes, name='reportes'),
    path('agregar/', views.agregar, name='agregar'),  # Asegúrate de que esta existe
]
