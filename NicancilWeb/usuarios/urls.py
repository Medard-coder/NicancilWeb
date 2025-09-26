# usuarios/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('', views.login_view, name='root'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('registro/', views.registro_view, name='registro'),
    path('perfil/', views.editar_perfil, name='editar_perfil'),
]
