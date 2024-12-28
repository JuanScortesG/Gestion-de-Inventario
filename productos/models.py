from django.db import models
from django.core.validators import MinValueValidator, RegexValidator
from django.core.exceptions import ValidationError
from django.utils import timezone

# Create your models here.
class Categoria(models.Model):
    #* identificador
    id = models.AutoField(primary_key=True)
    
    #* Datos
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True, max_length=500)
    
    #* Campos de gestion
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ['nombre']
    
    #* Metodo personalizado de validacion
    def clean(self):
        self.nombre = self.nombre.strip().title()
        

class Producto(models.Model):
    SKU_REGEX = r'^[A-Z]{2}\d{6}$'
    sku = models.CharField(
        max_length = 8,
        unique = True,
        validators = [RegexValidator(
            SKU_REGEX,
            message = "The SKU must be have 2 letters following 6 digits"
        )]
    )
    nombre = models.CharField(max_length=200)
    #* Reemplazado por SKU
    #codigo = models.CharField(max_length=50, unique=True)
    
    #* Relaciones
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        null=True,
        related_name='productos'
    )
    
    #* Campos financieros
    precio_compra = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        #validators=[MinValueValidator(0)]
    )
    precio_venta = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        #validators=[MinValueValidator(0)]
    )
    
    #* Campos de control
    active = models.BooleanField(default = True)
    fecha_creacion = models.DateTimeField(auto_now_add =True)
    
    def __str__(self):
        return f'{self.nombre} ({self.sku})'
    
    def clean(self):
        if self.precio_venta <= self.precio_compra:
            raise ValidationError(
                "the sell price must be greather than the buy price")
    
class Inventario(models.Model):
    #* Relaciones
    producto = models.OneToOneField(
        Producto,
        on_delete=models.CASCADE,
        related_name='inventario'
    )
    
    #* Campos de stock
    stock = models.PositiveIntegerField(default=0)
    stock_minimo = models.PositiveIntegerField(default=10)
    stock_maximo = models.PositiveIntegerField(default=100)
    
    #* Campos de seguimiento
    last_update = models.DateField(auto_now=True)
    date_last_inventory = models.DateTimeField(null=True, blank=True)
    
    #* Campus calculados
    @property
    def non_available(self):
        return self.stock <= self.min_stock
    
    def update_stock(self, quantity):
        if self.stock + quantity < 0:
            raise ValueError ("No hay suficiente stock")
        
        self.stock += quantity
        self.save()
    
    
    def __str__(self):
        return f'Stock de {self.producto.nombre}'
    
    class Meta:
        verbose_name = "Inventario"
        verbose_name_plural = "Inventarios"
    
    def clean(self):
        if self.stock_minimo >= self.stock_maximo:
            raise ValidationError(
                "El stock minimo debe ser menor al stock maximo")

