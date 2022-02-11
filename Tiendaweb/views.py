from django.db.utils import OperationalError
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, reverse 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import *


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
    
    # Sección de Login
    if request.method == 'POST':
        username = request.POST.get('singin-email') 
        password = request.POST.get('singin-password')
        
        # Verificar que existe esas credenciales y devuelve un objeto "Usuario"
        user = authenticate(username=username, password=password)
        
        # Si existe ese objeto..
        if user is not None:
            # Se lo loguea en la sesion actual
            login(request, user)

    return render(request, 'home.html', {'sellitemsh':sellitemsh,'sellitemsm':sellitemsm, 'sellitemsw':sellitemsw,'sellitems':sellitems, 
        'items':newitems, 'ListaCategoria':obtener_categoria(), 'context':obtener_carrito(request), 
        'contextfav':obtener_favoritos(request)})

def shoplist(request):
    return render(request, 'shop.html')

def categorylist(request):
    return render(request, 'category-list.html')




########################################################################################################################
#                                               Log in y log out                                                       #
########################################################################################################################

@login_required
def log_user_out(request):
    logout(request)
    return redirect('home')
