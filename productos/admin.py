from django.contrib import admin
from .models import Categoria, Producto, Inventario

# Register your models here.
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id','nombre', 'descripcion', 'fecha_creacion')
    search_fields = ('nombre',)

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('sku','nombre', 'active', 'categoria', 'precio_venta')
    list_filter = ('categoria','active')
    search_fields = ('sku', 'name')

@admin.register(Inventario)
class InventarioAdmin(admin.ModelAdmin):
    list_display = ('producto', 'stock', 'stock_minimo',
                    'stock_maximo', 'non_available')