from django.db.utils import OperationalError
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from .models import *
from .forms import *
from django.db.models import Count

import logging


########################################################################################################################
#                                                Funciones generales                                                   #
########################################################################################################################

def obtener_categoria():  # Buscamos los productos (primeros 8), esto es solo para la pestaña productos
	catlist = Categoria.objects.all()[:8]
	return catlist


def obtener_carrito(request):  #Devuelve el carrito y sus items del usuario
	if request.user.is_authenticated:
		carrito, created = Carrito.objects.get_or_create(usuario=request.user)
		items = ItemCarrito.objects.filter(carrito=carrito)
		cantidad = ItemCarrito.objects.filter(carrito=carrito).count()
		context = {'carrito':carrito,
		'items': items, 'cantidad':cantidad}
	else:
		context = None
	return context


def obtener_favoritos(request): #Devuelve los favoritos marcados por el usuario
	if request.user.is_authenticated:
		fav = Favorito.objects.filter(usuario=request.user)
		cantidad = Favorito.objects.filter(usuario=request.user).count()
		contextfav = {'fav':fav,
		'cantidad': cantidad}
	else:
		contextfav = None
	return contextfav



########################################################################################################################
#                                               Funciones para vistas                                                  #
########################################################################################################################


def home(request):
	# Sección de datos
	newitems = Producto.objects.order_by('fecha_alta')[:10]
	sellitems = Imagene.objects.all().select_related('producto').order_by('-producto__Vendidos')[:10]
	sellitemsh = Imagene.objects.all().select_related('producto').order_by('-producto__fecha_alta')[:10]

	context = {
		'sellitemsh':sellitemsh,
		'sellitems':sellitems,
		'items':newitems
	}

	return render(request, 'home.html', {'context':context, 
		'Favorito':obtener_favoritos(request),
		'Carrito':obtener_carrito(request),
		'ListaCategoria':obtener_categoria()}
	)

def shoplist(request):
	#col = None
	cat = tam = mar = None
	Products = Imagene.objects.all().select_related('producto')
	Product_List = Imagene.objects.all().select_related('producto')
	#if request.GET.get('Color'):
	#	col = request.GET.get('Color')
	#	request.session['Color'] = col
	#	Product_List = Product_List.filter(producto__Color=col)
	if request.GET.get('Tamanio'):
		tam = request.GET.get('Tamanio')
		fil = 'producto__' + tam + '__gt'
		Product_List = Product_List.filter(**{ fil: 0 })
	if request.GET.get('Categoria'):
		cat = request.GET.get('Categoria')
		request.session['Categoria'] = cat
		Product_List = Product_List.filter(producto__Categoria=cat)
	if request.GET.get('Marca'):
		mar = request.GET.get('Marca')
		request.session['Marca'] = mar
		Product_List = Product_List.filter(producto__Marca=mar)
	if request.GET.get('Precio'):
		pre = request.GET.get('Precio')
		if pre == 'Precio-1':
			aux = Product_List.filter(producto__Precio_desc__gt=0, producto__Precio_desc__lte=100, producto__Precio=0)
			aux1 = Product_List.filter(producto__Precio__gt=0, producto__Precio__lte=100, producto__Precio_desc=0)
			Product_List = aux.union(aux1)
		elif pre == 'Precio-2':
			aux = Product_List.filter(producto__Precio_desc__gt=100, producto__Precio_desc__lte=200, producto__Precio=0)
			aux1 = Product_List.filter(producto__Precio__gt=100, producto__Precio__lte=200, producto__Precio_desc=0)
			Product_List = aux.union(aux1)
		elif pre == 'Precio-3':
			aux = Product_List.filter(producto__Precio_desc__gt=200, producto__Precio_desc__lte=300, producto__Precio=0)
			aux1 = Product_List.filter(producto__Precio__gt=200, producto__Precio__lte=300, producto__Precio_desc=0)
			Product_List = aux.union(aux1)
		elif pre == 'Precio-4':
			aux = Product_List.filter(producto__Precio_desc__gt=300, producto__Precio_desc__lte=400, producto__Precio=0)
			aux1 = Product_List.filter(producto__Precio__gt=300, producto__Precio__lte=400, producto__Precio_desc=0)
			Product_List = aux.union(aux1)
		elif pre == 'Precio-5':
			aux = Product_List.filter(producto__Precio_desc__gt=400, producto__Precio_desc__lte=500, producto__Precio=0)
			aux1 = Product_List.filter(producto__Precio__gt=400, producto__Precio__lte=500, producto__Precio_desc=0)
			Product_List = aux.union(aux1)
	if request.GET.get('Orden'):
		order = request.GET.get('Orden')
		if order == 'Lastest':
			Product_List = Product_List.order_by('-producto__fecha_alta')
		elif order == 'BestRating':
			Product_List = Product_List.order_by('-producto__Vendidos')

	page = request.GET.get('page', 1)
	paginator = Paginator(Product_List, 12)

	try:
		page_obj = paginator.page(page)
	except PageNotAnInteger:
		page_obj = paginator.page(1)
	except EmptyPage:
		page_obj = paginator.page(paginator.num_pages)
	context = {
		#'Col_Sort':Colore.objects.values('Nombre').annotate(total=Count('Nombre')).order_by(),
		'Mar_Sort':Marca.objects.values('Nombre').annotate(total=Count('Nombre')).order_by(),
		'Cat_Sort':Categoria.objects.all().order_by('Nombre'),		
		'cat':cat, 'tam':tam, #'col':col
		'mar':mar, 'page_obj':page_obj,
	}
	
	return render(request, 'shop.html', {'context':context,
		'Favorito':obtener_favoritos(request),
		'Carrito':obtener_carrito(request),
		'ListaCategoria':obtener_categoria()})

def shoprod(request, Codigo):
	context = {
		'items_similares' : Imagene.objects.all().select_related('producto').exclude(producto=Codigo).distinct()[:8]
	}

	return render(request, 'detail.html', {'context':context,
		'Product' : Imagene.objects.filter(producto=Codigo).select_related('producto').get(),
		'Favorito':obtener_favoritos(request),
		'Carrito':obtener_carrito(request),
		'ListaCategoria':obtener_categoria()})


def addcarrito(request, Codigo):
	size = request.POST.get('size-opt')
	cant = request.POST.get('cantidad')


	return redirect('shop-prod')

def carrito(request):
	return render(request, 'cart.html', {
		'Favorito':obtener_favoritos(request),
		'Carrito':obtener_carrito(request),
		'ListaCategoria':obtener_categoria()})

def categorylist(request):
	context = {
		'Favorito':obtener_favoritos(request),
		'carrito':obtener_carrito(request),
		'ListaCategoria':obtener_categoria()
	}
	return render(request, 'category-list.html', {'context':context})

def favoritos(request):
	pass

########################################################################################################################
#                                               Log in y log out                                                       #
########################################################################################################################

def Auth_login(request):
	F_Log = Login(request.POST or None)

	if request.method == 'POST':
		if '_singin' in request.POST:
			if F_Log.is_valid():
				user = authenticate(username=F_Log.cleaned_data['username'], password=F_Log.cleaned_data['password'])
				if user is not None:
					login(request, user)
					return redirect('home')
				else:
					messages.warning(request, "Credenciales inválidas." )
					return redirect('login')
		else:
			if F_Log.is_valid():
				if User.objects.filter(username = F_Log.cleaned_data['username']).first():
					messages.error(request, "Usuario ya ocupado")
					return redirect('login')
				user = User.objects.create_user(F_Log.cleaned_data['username'], '', F_Log.cleaned_data['password'])
				user.save()
				login(request, user)
				return redirect('home')

	return render(request, 'login.html', {'F_Log':F_Log})


@login_required
def log_user_out(request):
	logout(request)
	return redirect('home')
