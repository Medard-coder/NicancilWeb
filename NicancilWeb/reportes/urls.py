from django.urls import path
from . import views

urlpatterns = [
    path('', views.reportes_ventas, name='reportes_ventas'),
    path('pdf/', views.generar_reporte_pdf, name='generar_reporte_pdf'),
]