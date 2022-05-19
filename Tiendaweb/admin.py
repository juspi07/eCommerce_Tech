from django.contrib import admin
from image_cropping import ImageCroppingMixin

from .models import *

# Register your models here.

@admin.register(Categoria)
class ArticuloAdmin(admin.ModelAdmin):
	list_display = ('Nombre',)

@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
	list_display = ('Nombre',)

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
	list_display = ('Codigo', 'Marca', 'Categoria', 'Temporada', 'Ano', 'S', 'M', 'L', 'XL', 'XXL')

	list_filter = ('Marca', 'Categoria', 'Ano', 'Temporada')

	fieldsets = (
		(None, {
			'fields': ('Codigo', 'Nombre', 'Desc', 'Marca', 'Ano', 'Categoria', 'Temporada', 'Sexo', 'Vendidos', 'Precio', 'Precio_desc', 'fecha_alta')
		}),
		('Talles', {
			'fields': (('S', 'M', 'L'), ('XL', 'XXL'))
		}),
	)

	readonly_fields=('fecha_alta',)


	def save_model(self, request, obj, form, change):
		obj.Categoria.Cantidad += 1
		obj.Categoria.save()
		super().save_model(request, obj, form, change)

	def delete_model(self, request, obj):
		obj.Categoria.Cantidad -= 1
		obj.Carrito.save()
		super().delete_model(request, obj)


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
	