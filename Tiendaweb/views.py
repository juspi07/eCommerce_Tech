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
		context = {'carrito':carrito,
		'items': items}
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
	sellitemsm = Imagene.objects.filter(producto__Sexo='M').select_related('producto').order_by('-producto__Vendidos')[:5]
	sellitemsw = Imagene.objects.filter(producto__Sexo='F').select_related('producto').order_by('-producto__Vendidos')[:5]
	sellitemsh = Imagene.objects.all().select_related('producto').order_by('-producto__fecha_alta')[:10]

	return render(request, 'home.html', {'sellitemsh':sellitemsh,'sellitemsm':sellitemsm, 'sellitemsw':sellitemsw,'sellitems':sellitems, 
		'items':newitems, 'ListaCategoria':obtener_categoria(), 'context':obtener_carrito(request), 
		'contextfav':obtener_favoritos(request)})

def shoplist(request):
	cat = mar = col = None
	Product_List = Imagene.objects.all().select_related('producto')

	if 'categoria' in request.session:
		cat = request.session['categoria']
		Product_List = Product_List.filter(Categoria=cat)
	if 'marca' in request.session:
		mar = request.session['marca']
		Product_List = Product_List.filter(Categoria=mar)
	if 'color' in request.session:
		col = request.session['color']
		Product_List = Product_List.filter(Categoria=col)

	page = request.GET.get('page', 1)
	paginator = Paginator(Product_List, 10)

	try:
		page_obj = paginator.page(page)
	except PageNotAnInteger:
		page_obj = paginator.page(1)
	except EmptyPage:
		page_obj = paginator.page(paginator.num_pages)

	context = {
		'Mar_Sort':Marca.objects.all(),
		'Col_Sort':Colore.objects.all(),
		'Cat_Sort':Categoria.objects.all(),
		'cat':cat,
		'mar':mar,
		'col':col,
		'page_obj':page_obj,
	}
	
	return render(request, 'shop.html', {'context':context})

def shoplistFCat(request, cat):
	request.session['categoria'] = cat
	return HttpResponseRedirect(reverse('shop'))

def shoplistFMar(request, mar):
	request.session['marca'] = mar
	HttpResponseRedirect(reverse('shop'))

def shoplistFCol(request, col):
	request.session['color'] = col
	HttpResponseRedirect(reverse('shop'))

def categorylist(request):
	return render(request, 'category-list.html')




########################################################################################################################
#                                               Log in y log out                                                       #
########################################################################################################################

def Auth_login(request):
	F_Reg = Register(request.POST or None)
	F_Log = Login(request.POST or None)

	if request.method == 'POST':
		if '_singup' in request.POST:
			if F_Log.is_valid():
				user = authenticate(username=F_Log.cleaned_data['username'], password=F_Log.cleaned_data['password'])
				if user is not None:
					login(request, user)
					return redirect('home')
				else:
					messages.warning(request, "Credenciales inválidas." )
					return redirect('login')
		else:
			if F_Reg.is_valid():
				if User.objects.filter(username = F_Reg.cleaned_data['username']).first():
					messages.error(request, "Usuario ya ocupado")
					return redirect('login')
				user = User.objects.create_user(F_Reg.cleaned_data['username'], '', F_Reg.cleaned_data['password'])
				user.save()
				login(request, user)
				return redirect('home')

	return render(request, 'login.html', {'F_Reg' :F_Reg, 'F_Log':F_Log})


@login_required
def log_user_out(request):
	logout(request)
	return redirect('home')
