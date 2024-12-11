from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .models import Producto, Cliente, Pedido, Proveedor, Envio
from .serializers import ProductoSerializer, ClienteSerializer, PedidoSerializer, ProveedorSerializer, EnvioSerializer
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import render, get_object_or_404, redirect
from .forms import ProductoForm
import csv
from django.views.decorators.csrf import csrf_exempt

# Vista para login
@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            return JsonResponse({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=200)
        else:
            return JsonResponse({"error": "Credenciales incorrectas."}, status=400)
    return JsonResponse({"error": "Método no permitido."}, status=405)

# Vista para registro
@csrf_exempt
def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST.get('email', '')
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()
            return JsonResponse({"message": "Usuario registrado exitosamente."}, status=201)
        else:
            return JsonResponse({"error": "El usuario ya existe."}, status=400)
    return JsonResponse({"error": "Método no permitido."}, status=405)

# Vista para exportar productos a CSV
def export_productos_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="productos.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID', 'Nombre', 'Descripción', 'Precio', 'Inventario', 'Categoría'])

    productos = Producto.objects.all()
    for producto in productos:
        writer.writerow([
            producto.id, 
            producto.nombre, 
            producto.descripcion, 
            producto.precio, 
            producto.inventario, 
            producto.categoria
        ])

    return response

# Vista para listar productos
def productos_list(request):
    if request.method == 'GET':
        productos = Producto.objects.all()
        return render(request, 'productos/productos_list.html', {'productos': productos})

# Vista para el detalle de un producto
def producto_detail(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    return render(request, 'productos/producto_detail.html', {'producto': producto})

# Vista para crear productos
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('productos-list')
    else:
        form = ProductoForm()
    return render(request, 'productos/crear_producto.html', {'form': form})

# Vista para actualizar productos
def actualizar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('productos-list')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'productos/actualizar_producto.html', {'form': form, 'producto': producto})

# Vista para eliminar productos
def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        return redirect('productos-list')
    return render(request, 'productos/eliminar_producto.html', {'producto': producto})

# Vistas ViewSet de Django REST Framework para CRUD API con filtros
class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, pk=None):
        producto = get_object_or_404(Producto, pk=pk)
        serializer = self.get_serializer(producto)
        return Response(serializer.data)

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [IsAuthenticated]

class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    permission_classes = [IsAuthenticated]

class ProveedorViewSet(viewsets.ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer
    permission_classes = [IsAuthenticated]

class EnvioViewSet(viewsets.ModelViewSet):
    queryset = Envio.objects.all()
    serializer_class = EnvioSerializer
    permission_classes = [IsAuthenticated]
