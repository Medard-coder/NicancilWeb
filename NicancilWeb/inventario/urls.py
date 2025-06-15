from django.urls import path
from . import views

urlpatterns = [
    path('tienda/', views.lista_prendas, name='lista_prendas'),
    path('prenda/<int:pk>/', views.detalle_prendas, name='detalle_prendas'),
    path('nueva_prenda/', views.nueva_prenda, name='nueva_prenda'),
    path('editar_prenda/<int:pk>/', views.editar_prenda, name='editar_prenda'),
    path('eliminar_prenda/<int:pk>/', views.eliminar_prenda, name='eliminar_prenda'),
    path('inventario/', views.inventario, name='inventario'),
]