from django.contrib import admin
from django.utils.html import format_html
from .models import Categoria, Producto, ProductoImagen

class ProductoImagenInline(admin.TabularInline):
    model = ProductoImagen
    extra = 1

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'activo', 'fecha_creacion']
    list_filter = ['activo', 'fecha_creacion']
    search_fields = ['nombre']
    prepopulated_fields = {'slug': ('nombre',)}

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'categoria', 'precio', 'disponible', 'destacado', 'imagen_preview']
    list_filter = ['categoria', 'disponible', 'destacado', 'fecha_creacion']
    search_fields = ['nombre', 'descripcion']
    prepopulated_fields = {'slug': ('nombre',)}
    list_editable = ['precio', 'disponible', 'destacado']
    inlines = [ProductoImagenInline]
    
    def imagen_preview(self, obj):
        if obj.imagen:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.imagen.url)
        return "Sin imagen"
    imagen_preview.short_description = "Vista previa"

@admin.register(ProductoImagen)
class ProductoImagenAdmin(admin.ModelAdmin):
    list_display = ['producto', 'imagen_preview', 'orden']
    list_filter = ['producto']
    
    def imagen_preview(self, obj):
        if obj.imagen:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.imagen.url)
        return "Sin imagen"
    imagen_preview.short_description = "Vista previa"
