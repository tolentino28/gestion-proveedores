from django.contrib import admin
from .models import Proveedor, Producto, Compra, Cuota, Pago

admin.site.register(Proveedor)
admin.site.register(Producto)
admin.site.register(Compra)
admin.site.register(Cuota)
admin.site.register(Pago)
