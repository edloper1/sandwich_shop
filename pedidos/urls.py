from django.urls import path
from . import views

app_name = 'pedidos'

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('confirmacion/<uuid:numero_pedido>/', views.confirmacion_pedido, name='confirmacion'),
    path('seguimiento/<uuid:numero_pedido>/', views.seguimiento_pedido, name='seguimiento'),
    path('mis-pedidos/', views.mis_pedidos, name='mis_pedidos'),
]