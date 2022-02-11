from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MinValueValidator
from django.contrib.auth.models import User
from image_cropping import ImageRatioField
from datetime import *

# Create your models here.

Temporada = (
	('V', 'Primavera - Verano'),
	('I', 'Otoño - Invierno'),
)

Sexo = (
	('M', 'Masculino'),
	('F', 'Femenino'),
)

class Marca(models.Model):
	Nombre = models.CharField(max_length=30, primary_key=True)

	def __str__(self):
		return self.Nombre 

class Categoria(models.Model):
	Nombre = models.CharField(max_length=30, primary_key=True)

	def __str__(self):
		return self.Nombre 

class Colore(models.Model):
	Nombre = models.CharField(max_length=15, primary_key=True)

	def __str__(self):
		return self.Nombre

class Producto(models.Model):
	Codigo = models.CharField(max_length=10, validators=[MinLengthValidator(10, 'Codigo inválido')], primary_key=True)
	Marca = models.ForeignKey('Marca',on_delete=models.RESTRICT)
	Ano = models.DecimalField('Año', max_digits=4, decimal_places=0)
	Categoria = models.ForeignKey('Categoria',on_delete=models.RESTRICT)
	Color = models.ForeignKey('Colore',on_delete=models.RESTRICT)
	Temporada = models.CharField(max_length=1, choices=Temporada)
	Sexo = models.CharField(max_length=1, choices=Sexo)
	fecha_alta = models.DateField('Fecha de Alta:', auto_now_add=True) 
	Precio = models.DecimalField('Precio:', max_digits=9, decimal_places=2, validators=[MinValueValidator(0.01)])
	Precio_desc = models.DecimalField('Precio Descuento:', max_digits=9, decimal_places=2, default=0)
	Vendidos = models.DecimalField(default= 0, max_digits=4, decimal_places=0)
	S = models.IntegerField()
	M = models.IntegerField()
	L = models.IntegerField()
	XL = models.IntegerField()
	XXL = models.IntegerField()


class Imagene(models.Model):
	producto = models.ForeignKey(Producto, null=False, on_delete=models.CASCADE)
	Img1 = models.ImageField('Imagen Principal:', upload_to='img_productos/', default='')
	Recorte1 = ImageRatioField('Img1', '277x377')
	Img2 = models.ImageField('Imagen 2:', upload_to='img_productos/', default='')
	Recorte2 = ImageRatioField('Img2', '277x377')

	def __str__(self):
		return self.producto.Codigo

class Carrito(models.Model):
	usuario = models.OneToOneField(User, on_delete=models.CASCADE)
	cantidad = models.PositiveIntegerField(default=0)
	total = models.DecimalField('Total:', max_digits=9, decimal_places=2, default=0, validators=[MinValueValidator(0)])

	def __str__(self):
		return "{}".format(self.usuario)

class ItemCarrito(models.Model):
	carrito = models.ForeignKey(Carrito, null=False, on_delete=models.CASCADE)
	producto = models.ForeignKey(Producto, null=False, on_delete=models.CASCADE)
	cantidad = models.PositiveIntegerField(default=1)
	subtotal = models.DecimalField('Subtotal:', max_digits=9, decimal_places=2, default=0)

	class Meta:
		constraints = [
			models.UniqueConstraint(fields=['carrito', 'producto'], name='carrito_prod')
		]

	def __str__(self):
		return "Carrito: {}. Contenido: {} {}-{}(s).".format(self.carrito.usuario,
			self.cantidad, self.producto.marca, self.producto.categoria)


class Favorito(models.Model):
	usuario = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
	producto = models.OneToOneField(Producto, null=False, on_delete=models.CASCADE)