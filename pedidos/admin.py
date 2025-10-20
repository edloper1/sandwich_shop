from django.contrib import admin
from django.utils.html import format_html
from .models import Pedido, PedidoItem

class PedidoItemInline(admin.TabularInline):
    model = PedidoItem
    extra = 0
    readonly_fields = ['precio_unitario']

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ['numero_corto', 'nombre_cliente', 'estado', 'tipo_entrega', 'total', 'fecha_pedido']
    list_filter = ['estado', 'tipo_entrega', 'fecha_pedido']
    search_fields = ['numero_pedido', 'nombre_cliente', 'email_cliente', 'telefono_cliente']
    readonly_fields = ['numero_pedido', 'fecha_pedido']
    list_editable = ['estado']
    inlines = [PedidoItemInline]
    
    fieldsets = (
        ('Información del Pedido', {
            'fields': ('numero_pedido', 'estado', 'fecha_pedido', 'fecha_estimada_entrega', 'fecha_entrega')
        }),
        ('Información del Cliente', {
            'fields': ('usuario', 'nombre_cliente', 'email_cliente', 'telefono_cliente')
        }),
        ('Entrega', {
            'fields': ('tipo_entrega', 'direccion_entrega')
        }),
        ('Totales', {
            'fields': ('subtotal', 'costo_delivery', 'total')
        }),
        ('Notas', {
            'fields': ('notas_cliente', 'notas_internas')
        }),
    )

@admin.register(PedidoItem)
class PedidoItemAdmin(admin.ModelAdmin):
    list_display = ['pedido', 'producto', 'cantidad', 'precio_unitario', 'total_precio']
    list_filter = ['pedido__fecha_pedido', 'producto__categoria']
    search_fields = ['pedido__numero_pedido', 'producto__nombre']
