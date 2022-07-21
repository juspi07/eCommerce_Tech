"""eCommerce_Tech URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
"""  """


from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.urls import *
from django.conf.urls import url

from Tiendaweb import views

urlpatterns = [
    path('', views.home, name='home'),
    
    path('shop/', views.shoplist, name='shop-list'),
    re_path(r'^shop/(?P<query>\w+)$', views.shoplist, name='shop-list'),
   
    path('shop/producto/<str:Codigo>', views.shoprod, name='shop-prod'),

    path('categorias/', views.categorylist, name='category-list'),
    
    path('favoritos/', views.favoritos, name='favoritos'),

    path('admin/', admin.site.urls),
    path('logout/', views.log_user_out, name='logout'),
    path('login/', views.Auth_login, name='login'),
    path('cart/', views.carrito, name='cart'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
