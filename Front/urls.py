from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.Inicio, name='Inicio'),
    path('información/', views.Información, name='Información'),
    path('contacto/', views.Contacto, name='Contacto'),

    path('iniciarSesion/', views.IniciarSesión, name='IniciarSesión'),
    path('registro/', views.registro, name='Registro'),

    path('registrarProductoBienvenida/', views.RegistroProductoBienvenida, name='RegistroProductoBienvenida'),
    path('registroProducto/', views.RegistroProducto, name='RegistroProducto'),

    path('proveedores/', views.Proveedores, name='Proveedores'),
    path('registroProveedor/', views.RegistrarOEditarProveedor, name='registro_proveedor'),
    path('editarProveedor/<int:id_proveedor>/', views.RegistrarOEditarProveedor, name='editar_proveedor'),
    path('proveedor/eliminar/<int:id_proveedor>/', views.EliminarProveedor, name='eliminar_proveedor'),
    
    path('compras/', views.Compras, name='Compras'),
    path('formularioCompra/', views.FormularioCompra, name='FormularioCompra'),
    path('compra/eliminar/<int:id_compra>/', views.EliminarCompra, name='eliminar_compra'),
    
    path('api/cuotas/<int:compra_id>/', views.obtener_cuotas, name='obtener_cuotas'),
    path('api/pagos/<int:cuota_id>/', views.registrar_pago, name='registrar_pago'),

    path('perfil/', views.Perfil, name='Perfil'),
   
    path('cerrarSesion/', views.CerrarSesion, name='CerrarSesion'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    