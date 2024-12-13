from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.
class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name_plural = "Categorias"
    
class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    codigo = models.CharField(max_length=50, unique=True)
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        null=True,
        related_name='productos'
    )
    precio_compra = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    precio_venta = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    
    def __str__(self):
        return f'{self.nombre} ({self.codigo})'
    
class Inventario(models.Model):
    producto = models.OneToOneField(
        Producto,
        on_delete=models.CASCADE,
        related_name='inventario'
    )
    cantidad_stock = models.PositiveIntegerField(default=0)
    stock_minimo = models.PositiveIntegerField(default=10)
    
    def __str__(self):
        return f'Stock de {self.producto.nombre}'
    
    class Meta:
        verbose_name_plural = "Inventarios"

