from django.core.management.base import BaseCommand
from django.core.files import File
from productos.models import Categoria, Producto
import os
import glob
from decimal import Decimal
import random

class Command(BaseCommand):
    help = 'Poblar la base de datos con productos de ejemplo usando las imágenes disponibles'

    def handle(self, *args, **options):
        self.stdout.write('Iniciando población de datos...')
        
        # Crear categorías
        categorias_data = [
            {
                'nombre': 'Clásicos',
                'descripcion': 'Nuestros sándwiches tradicionales y más populares'
            },
            {
                'nombre': 'Gourmet',
                'descripcion': 'Sándwiches premium con ingredientes selectos'
            },
            {
                'nombre': 'Vegetarianos',
                'descripcion': 'Opciones deliciosas sin carne'
            },
            {
                'nombre': 'Especiales',
                'descripcion': 'Creaciones únicas de la casa'
            },
            {
                'nombre': 'Ligeros',
                'descripcion': 'Opciones saludables y bajas en calorías'
            }
        ]
        
        categorias = {}
        for cat_data in categorias_data:
            categoria, created = Categoria.objects.get_or_create(
                nombre=cat_data['nombre'],
                defaults={'descripcion': cat_data['descripcion']}
            )
            categorias[cat_data['nombre']] = categoria
            if created:
                self.stdout.write(f'Categoría creada: {categoria.nombre}')
        
        # Nombres de sándwiches para generar
        sandwiches_data = [
            {
                'nombre': 'Club Sandwich Clásico',
                'descripcion': 'Triple piso con pavo, tocino, lechuga, tomate y mayonesa en pan tostado.',
                'categoria': 'Clásicos',
                'precio': 12.99,
                'ingredientes': 'Pavo, Tocino, Lechuga, Tomate, Mayonesa, Pan Integral',
                'tiempo_preparacion': 15,
                'destacado': True
            },
            {
                'nombre': 'Hamburguesa BBQ Premium',
                'descripcion': 'Carne de res angus con salsa BBQ, cebolla caramelizada y queso cheddar.',
                'categoria': 'Gourmet',
                'precio': 15.99,
                'ingredientes': 'Carne Angus, Salsa BBQ, Cebolla Caramelizada, Queso Cheddar, Pan Brioche',
                'tiempo_preparacion': 20,
                'destacado': True
            },
            {
                'nombre': 'Sandwich Veggie Deluxe',
                'descripcion': 'Aguacate, hummus, pepino, tomate, brotes y lechuga en pan multicereales.',
                'categoria': 'Vegetarianos',
                'precio': 10.99,
                'ingredientes': 'Aguacate, Hummus, Pepino, Tomate, Brotes, Lechuga, Pan Multicereales',
                'tiempo_preparacion': 10,
                'destacado': True
            },
            {
                'nombre': 'Wrap de Pollo Cajún',
                'descripcion': 'Pollo especiado estilo cajún con verduras frescas en tortilla de espinaca.',
                'categoria': 'Especiales',
                'precio': 13.99,
                'ingredientes': 'Pollo Cajún, Pimientos, Cebolla, Lechuga, Tortilla de Espinaca',
                'tiempo_preparacion': 18,
                'destacado': False
            },
            {
                'nombre': 'Sandwich de Jamón y Queso',
                'descripcion': 'Jamón de pavo, queso suizo, mostaza y pepinillos en pan de centeno.',
                'categoria': 'Clásicos',
                'precio': 9.99,
                'ingredientes': 'Jamón de Pavo, Queso Suizo, Mostaza, Pepinillos, Pan de Centeno',
                'tiempo_preparacion': 12,
                'destacado': False
            },
            {
                'nombre': 'Panini Caprese',
                'descripcion': 'Mozzarella fresca, tomate, albahaca y aceite de oliva en pan ciabatta.',
                'categoria': 'Vegetarianos',
                'precio': 11.99,
                'ingredientes': 'Mozzarella, Tomate, Albahaca, Aceite de Oliva, Pan Ciabatta',
                'tiempo_preparacion': 15,
                'destacado': False
            },
            {
                'nombre': 'Sandwich de Atún Mediterráneo',
                'descripcion': 'Atún, aceitunas, tomate seco, rúcula y vinagreta mediterránea.',
                'categoria': 'Ligeros',
                'precio': 12.49,
                'ingredientes': 'Atún, Aceitunas, Tomate Seco, Rúcula, Vinagreta, Pan Integral',
                'tiempo_preparacion': 13,
                'destacado': False
            },
            {
                'nombre': 'Burger de Salmón',
                'descripcion': 'Filete de salmón a la parrilla con aguacate y salsa tártara especial.',
                'categoria': 'Gourmet',
                'precio': 17.99,
                'ingredientes': 'Salmón, Aguacate, Salsa Tártara, Lechuga, Pan Brioche',
                'tiempo_preparacion': 22,
                'destacado': True
            },
            {
                'nombre': 'Sandwich Cubano',
                'descripcion': 'Cerdo asado, jamón, queso suizo, pepinillos y mostaza en pan cubano.',
                'categoria': 'Especiales',
                'precio': 14.99,
                'ingredientes': 'Cerdo Asado, Jamón, Queso Suizo, Pepinillos, Mostaza, Pan Cubano',
                'tiempo_preparacion': 16,
                'destacado': False
            },
            {
                'nombre': 'Wrap Caesar de Pollo',
                'descripcion': 'Pollo a la parrilla, lechuga romana, parmesano y aderezo Caesar.',
                'categoria': 'Ligeros',
                'precio': 11.49,
                'ingredientes': 'Pollo, Lechuga Romana, Parmesano, Aderezo Caesar, Tortilla',
                'tiempo_preparacion': 14,
                'destacado': False
            }
        ]
        
        # Obtener lista de imágenes disponibles
        media_path = 'media/productos/'
        imagenes_disponibles = []
        if os.path.exists(media_path):
            imagenes_disponibles = [f for f in os.listdir(media_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        
        # Crear productos
        for i, producto_data in enumerate(sandwiches_data):
            categoria = categorias[producto_data['categoria']]
            
            # Verificar si el producto ya existe
            if not Producto.objects.filter(nombre=producto_data['nombre']).exists():
                # Seleccionar una imagen aleatoria si está disponible
                imagen_path = None
                if imagenes_disponibles and i < len(imagenes_disponibles):
                    imagen_filename = imagenes_disponibles[i]
                    imagen_path = f'productos/{imagen_filename}'
                
                producto = Producto.objects.create(
                    nombre=producto_data['nombre'],
                    descripcion=producto_data['descripcion'],
                    categoria=categoria,
                    precio=Decimal(str(producto_data['precio'])),
                    ingredientes=producto_data['ingredientes'],
                    tiempo_preparacion=producto_data['tiempo_preparacion'],
                    destacado=producto_data['destacado'],
                    disponible=True
                )
                
                # Asignar imagen si está disponible
                if imagen_path:
                    producto.imagen = imagen_path
                    producto.save()
                
                self.stdout.write(f'Producto creado: {producto.nombre}')
            else:
                self.stdout.write(f'Producto ya existe: {producto_data["nombre"]}')
        
        self.stdout.write(self.style.SUCCESS('¡Datos poblados exitosamente!'))
        self.stdout.write(f'Categorías: {Categoria.objects.count()}')
        self.stdout.write(f'Productos: {Producto.objects.count()}')