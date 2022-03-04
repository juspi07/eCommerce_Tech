from .models import Producto
import django_filters

class ProdFilter(django_filters.FilterSet):
    class Meta:
        model = Producto
        fields = ['Categoria','Marca','Color']