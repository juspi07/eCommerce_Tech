from django.contrib import admin
from image_cropping import ImageCroppingMixin

from .models import *

# Register your models here.

@admin.register(Colore)
class ColorAdmin(admin.ModelAdmin):
	list_display = ('Nombre',)

@admin.register(Categoria)
class ArticuloAdmin(admin.ModelAdmin):
	list_display = ('Nombre',)

@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
	list_display = ('Nombre',)

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
	list_display = ('Codigo', 'Marca', 'Categoria', 'Color', 'Temporada', 'Ano', 'S', 'M', 'L', 'XL', 'XXL')

	list_filter = ('Marca', 'Categoria', 'Color', 'Ano', 'Temporada')

	fieldsets = (
		(None, {
			'fields': ('Codigo', 'Nombre', 'Marca', 'Ano', 'Categoria', 'Color', 'Temporada', 'Sexo', 'Vendidos', 'Precio', 'Precio_desc')
		}),
		('Talles', {
			'fields': (('S', 'M', 'L'), ('XL', 'XXL'))
		}),
	)

@admin.register(ItemCarrito)
class ItemCarritoAdmin(admin.ModelAdmin):

	def save_model(self, request, obj, form, change):
		obj.carrito.total += obj.cantidad * obj.producto.precio
		obj.carrito.cantidad += obj.cantidad
		obj.carrito.save()
		super().save_model(request, obj, form, change)

	def delete_model(self, request, obj):
		obj.carrito.total -= obj.cantidad * obj.producto.precio
		obj.carrito.cantidad -= obj.cantidad
		obj.carrito.save()
		super().delete_model(request, obj)


@admin.register(Imagene)
class MyModelAdmin(ImageCroppingMixin, admin.ModelAdmin):
	pass



admin.site.register(Carrito)
admin.site.register(Favorito)
	