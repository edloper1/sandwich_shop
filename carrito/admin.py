from django.contrib import admin
from .models import Carrito, CarritoItem

class CarritoItemInline(admin.TabularInline):
    model = CarritoItem
    extra = 0
    readonly_fields = ['precio_unitario', 'fecha_agregado']

@admin.register(Carrito)
class CarritoAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'total_items', 'total_precio', 'fecha_creacion']
    list_filter = ['fecha_creacion']
    search_fields = ['usuario__username', 'session_key']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
    inlines = [CarritoItemInline]

@admin.register(CarritoItem)
class CarritoItemAdmin(admin.ModelAdmin):
    list_display = ['producto', 'carrito', 'cantidad', 'precio_unitario', 'total_precio']
    list_filter = ['fecha_agregado', 'producto__categoria']
    search_fields = ['producto__nombre', 'carrito__usuario__username']
    readonly_fields = ['fecha_agregado']
