from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from carrito.views import obtener_carrito
from .models import Pedido, PedidoItem
from .forms import CheckoutForm
from decimal import Decimal

def checkout(request):
    """Vista para procesar el checkout del carrito"""
    carrito = obtener_carrito(request)
    items = carrito.items.all()
    
    if not items:
        messages.error(request, 'Tu carrito está vacío')
        return redirect('carrito:ver_carrito')
    
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Crear el pedido
            pedido = Pedido.objects.create(
                usuario=request.user if request.user.is_authenticated else None,
                nombre_cliente=form.cleaned_data['nombre_cliente'],
                email_cliente=form.cleaned_data['email_cliente'],
                telefono_cliente=form.cleaned_data['telefono_cliente'],
                tipo_entrega=form.cleaned_data['tipo_entrega'],
                direccion_entrega=form.cleaned_data.get('direccion_entrega', ''),
                notas_cliente=form.cleaned_data.get('notas_cliente', ''),
                subtotal=carrito.total_precio,
                costo_delivery=Decimal('0.00') if form.cleaned_data['tipo_entrega'] == 'pickup' else Decimal('5.00'),
                total=carrito.total_precio + (Decimal('0.00') if form.cleaned_data['tipo_entrega'] == 'pickup' else Decimal('5.00'))
            )
            
            # Crear los items del pedido
            for item in items:
                PedidoItem.objects.create(
                    pedido=pedido,
                    producto=item.producto,
                    cantidad=item.cantidad,
                    precio_unitario=item.precio_unitario,
                    notas=item.notas
                )
            
            # Vaciar el carrito
            carrito.items.all().delete()
            
            messages.success(request, f'¡Pedido #{pedido.numero_corto} creado exitosamente!')
            return redirect('pedidos:confirmacion', numero_pedido=pedido.numero_pedido)
    else:
        initial_data = {}
        if request.user.is_authenticated:
            initial_data = {
                'nombre_cliente': f'{request.user.first_name} {request.user.last_name}'.strip() or request.user.username,
                'email_cliente': request.user.email,
            }
        form = CheckoutForm(initial=initial_data)
    
    context = {
        'form': form,
        'carrito': carrito,
        'items': items,
        'titulo': 'Finalizar Pedido'
    }
    return render(request, 'pedidos/checkout.html', context)

def confirmacion_pedido(request, numero_pedido):
    """Vista de confirmación del pedido"""
    try:
        pedido = Pedido.objects.get(numero_pedido=numero_pedido)
    except Pedido.DoesNotExist:
        raise Http404("Pedido no encontrado")
    
    context = {
        'pedido': pedido,
        'titulo': f'Confirmación - Pedido #{pedido.numero_corto}'
    }
    return render(request, 'pedidos/confirmacion.html', context)

def seguimiento_pedido(request, numero_pedido):
    """Vista para seguimiento del pedido"""
    try:
        pedido = Pedido.objects.get(numero_pedido=numero_pedido)
    except Pedido.DoesNotExist:
        raise Http404("Pedido no encontrado")
    
    context = {
        'pedido': pedido,
        'titulo': f'Seguimiento - Pedido #{pedido.numero_corto}'
    }
    return render(request, 'pedidos/seguimiento.html', context)

@login_required
def mis_pedidos(request):
    """Vista para mostrar los pedidos del usuario logueado"""
    pedidos = Pedido.objects.filter(usuario=request.user).order_by('-fecha_pedido')
    
    context = {
        'pedidos': pedidos,
        'titulo': 'Mis Pedidos'
    }
    return render(request, 'pedidos/mis_pedidos.html', context)
