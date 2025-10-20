from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from productos.models import Producto
from .models import Carrito, CarritoItem
import json

def obtener_carrito(request):
    """Obtiene o crea un carrito para el usuario/sesión actual"""
    if request.user.is_authenticated:
        carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        carrito, created = Carrito.objects.get_or_create(
            session_key=request.session.session_key
        )
    return carrito

def ver_carrito(request):
    """Vista para mostrar el contenido del carrito"""
    carrito = obtener_carrito(request)
    items = carrito.items.all()
    
    context = {
        'carrito': carrito,
        'items': items,
        'titulo': 'Mi Carrito'
    }
    return render(request, 'carrito/ver_carrito.html', context)

@require_POST
def agregar_al_carrito(request, producto_id):
    """Agregar un producto al carrito"""
    producto = get_object_or_404(Producto, id=producto_id, disponible=True)
    carrito = obtener_carrito(request)
    
    cantidad = int(request.POST.get('cantidad', 1))
    notas = request.POST.get('notas', '')
    
    try:
        item = CarritoItem.objects.get(carrito=carrito, producto=producto)
        item.cantidad += cantidad
        if notas:
            item.notas = notas
        item.save()
        messages.success(request, f'Se actualizó {producto.nombre} en tu carrito')
    except CarritoItem.DoesNotExist:
        CarritoItem.objects.create(
            carrito=carrito,
            producto=producto,
            cantidad=cantidad,
            precio_unitario=producto.precio,
            notas=notas
        )
        messages.success(request, f'{producto.nombre} se agregó a tu carrito')
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'total_items': carrito.total_items,
            'total_precio': float(carrito.total_precio)
        })
    
    return redirect('carrito:ver_carrito')

def actualizar_cantidad(request, item_id):
    """Actualizar la cantidad de un item en el carrito"""
    carrito = obtener_carrito(request)
    item = get_object_or_404(CarritoItem, id=item_id, carrito=carrito)
    
    if request.method == 'POST':
        cantidad = int(request.POST.get('cantidad', 1))
        if cantidad > 0:
            item.cantidad = cantidad
            item.save()
            messages.success(request, 'Cantidad actualizada correctamente')
        else:
            item.delete()
            messages.success(request, 'Producto eliminado del carrito')
    
    return redirect('carrito:ver_carrito')

def eliminar_del_carrito(request, item_id):
    """Eliminar un item del carrito"""
    carrito = obtener_carrito(request)
    item = get_object_or_404(CarritoItem, id=item_id, carrito=carrito)
    
    producto_nombre = item.producto.nombre
    item.delete()
    messages.success(request, f'{producto_nombre} eliminado del carrito')
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'total_items': carrito.total_items,
            'total_precio': float(carrito.total_precio)
        })
    
    return redirect('carrito:ver_carrito')

def vaciar_carrito(request):
    """Vaciar todo el carrito"""
    carrito = obtener_carrito(request)
    carrito.items.all().delete()
    messages.success(request, 'Carrito vaciado correctamente')
    return redirect('carrito:ver_carrito')

def obtener_info_carrito(request):
    """API para obtener información del carrito (AJAX)"""
    carrito = obtener_carrito(request)
    return JsonResponse({
        'total_items': carrito.total_items,
        'total_precio': float(carrito.total_precio)
    })
