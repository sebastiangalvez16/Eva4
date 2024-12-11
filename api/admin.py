from django.contrib import admin
from .models import Producto, Cliente, Pedido, Proveedor, Envio

# Register your models here.

admin.site.register(Producto)
admin.site.register(Cliente)
admin.site.register(Pedido)
admin.site.register(Proveedor)
admin.site.register(Envio)