from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Producto, Categoria

def inicio(request):
    """Vista principal que muestra productos destacados"""
    productos_destacados = Producto.objects.filter(disponible=True, destacado=True)[:6]
    categorias = Categoria.objects.filter(activo=True)
    
    context = {
        'productos_destacados': productos_destacados,
        'categorias': categorias,
        'titulo': 'Bienvenido a Sandwich Shop'
    }
    return render(request, 'productos/inicio.html', context)

def catalogo(request):
    """Vista del catálogo completo de productos"""
    productos = Producto.objects.filter(disponible=True)
    categorias = Categoria.objects.filter(activo=True)
    
    # Filtros
    categoria_id = request.GET.get('categoria')
    busqueda = request.GET.get('q')
    orden = request.GET.get('orden', 'nombre')
    
    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)
    
    if busqueda:
        productos = productos.filter(
            Q(nombre__icontains=busqueda) | 
            Q(descripcion__icontains=busqueda) |
            Q(ingredientes__icontains=busqueda)
        )
    
    # Ordenamiento
    if orden == 'precio_asc':
        productos = productos.order_by('precio')
    elif orden == 'precio_desc':
        productos = productos.order_by('-precio')
    elif orden == 'nombre':
        productos = productos.order_by('nombre')
    elif orden == 'fecha':
        productos = productos.order_by('-fecha_creacion')
    
    # Paginación
    paginator = Paginator(productos, 12)
    page_number = request.GET.get('page')
    productos_paginados = paginator.get_page(page_number)
    
    context = {
        'productos': productos_paginados,
        'categorias': categorias,
        'categoria_actual': categoria_id,
        'busqueda_actual': busqueda,
        'orden_actual': orden,
        'titulo': 'Catálogo de Productos'
    }
    return render(request, 'productos/catalogo.html', context)

def detalle_producto(request, slug):
    """Vista de detalle de un producto específico"""
    producto = get_object_or_404(Producto, slug=slug, disponible=True)
    productos_relacionados = Producto.objects.filter(
        categoria=producto.categoria, 
        disponible=True
    ).exclude(id=producto.id)[:4]
    
    context = {
        'producto': producto,
        'productos_relacionados': productos_relacionados,
        'titulo': producto.nombre
    }
    return render(request, 'productos/detalle_producto.html', context)

def categoria_productos(request, slug):
    """Vista de productos por categoría"""
    categoria = get_object_or_404(Categoria, slug=slug, activo=True)
    productos = Producto.objects.filter(categoria=categoria, disponible=True)
    
    # Paginación
    paginator = Paginator(productos, 12)
    page_number = request.GET.get('page')
    productos_paginados = paginator.get_page(page_number)
    
    context = {
        'categoria': categoria,
        'productos': productos_paginados,
        'titulo': f'Categoría: {categoria.nombre}'
    }
    return render(request, 'productos/categoria.html', context)
