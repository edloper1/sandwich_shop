from django.db import models
from django.contrib.auth.models import User
from productos.models import Producto
import uuid

class Pedido(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('confirmado', 'Confirmado'),
        ('preparando', 'Preparando'),
        ('listo', 'Listo para entrega'),
        ('entregado', 'Entregado'),
        ('cancelado', 'Cancelado'),
    ]
    
    TIPO_ENTREGA_CHOICES = [
        ('delivery', 'Delivery'),
        ('pickup', 'Recoger en tienda'),
    ]

    numero_pedido = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    # Información de contacto
    nombre_cliente = models.CharField(max_length=100)
    email_cliente = models.EmailField()
    telefono_cliente = models.CharField(max_length=20)
    
    # Información de entrega
    tipo_entrega = models.CharField(max_length=10, choices=TIPO_ENTREGA_CHOICES, default='pickup')
    direccion_entrega = models.TextField(blank=True)
    
    # Estado y fechas
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    fecha_estimada_entrega = models.DateTimeField(null=True, blank=True)
    fecha_entrega = models.DateTimeField(null=True, blank=True)
    
    # Totales
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    costo_delivery = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Notas
    notas_cliente = models.TextField(blank=True)
    notas_internas = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        ordering = ['-fecha_pedido']

    def __str__(self):
        return f'Pedido #{str(self.numero_pedido)[:8]} - {self.nombre_cliente}'

    @property
    def numero_corto(self):
        return str(self.numero_pedido)[:8].upper()

class PedidoItem(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    notas = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Item del Pedido'
        verbose_name_plural = 'Items del Pedido'

    def __str__(self):
        return f'{self.cantidad} x {self.producto.nombre}'

    @property
    def total_precio(self):
        return self.cantidad * self.precio_unitario
