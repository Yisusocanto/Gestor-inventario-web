from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("crear_usuario/", views.crear_usuario, name="crear_usuario"),
    path("ingresar/", views.ingresar, name="ingresar"),
    path("cerrar_sesion/", views.cerrar_sesion, name="cerrar_sesion"),
    path("pendiente/", views.pendiente, name="pendiente"),
    path("productos/", views.productos, name="productos"),
    path("crear_producto/", views.crear_producto, name="crear_producto"),
    path("productos/<int:producto_id>/", views.editar_producto, name="editar_producto"),
    path("productos/<int:producto_id>/eliminar", views.eliminar_producto, name="eliminar_producto"),
    path("productos/<int:producto_id>/vender", views.vender_producto, name="vender_producto"),
    path("ventas/", views.ventas, name="ventas"),
    ]