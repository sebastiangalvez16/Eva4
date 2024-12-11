from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProductoViewSet,
    ClienteViewSet,
    PedidoViewSet,
    ProveedorViewSet,
    EnvioViewSet,
    export_productos_csv,
    productos_list,
    producto_detail,
    crear_producto,
    actualizar_producto,
    eliminar_producto,
    register_view,
    login_view,
)

# Configuración del router
router = DefaultRouter()
router.register(r'productos', ProductoViewSet)
router.register(r'clientes', ClienteViewSet)
router.register(r'pedidos', PedidoViewSet)
router.register(r'proveedores', ProveedorViewSet)
router.register(r'envios', EnvioViewSet)

urlpatterns = [
    # Endpoint para exportar productos a CSV
    path('productos/exportar-csv/', export_productos_csv, name='export-productos-csv'),

    # Endpoints para vistas basadas en Django
    path('productos/list/', productos_list, name='productos-list'),
    path('productos/<int:pk>/', producto_detail, name='producto-detail'),
    path('productos/crear/', crear_producto, name='crear-producto'),
    path('productos/actualizar/<int:pk>/', actualizar_producto, name='actualizar-producto'),
    path('productos/eliminar/<int:pk>/', eliminar_producto, name='eliminar-producto'),

    # Endpoints de autenticación
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),

    # Rutas registradas en el router
    path('', include(router.urls)),
]
