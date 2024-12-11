from django.db import models

# Create your models here.

# Modelo de Producto
class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    inventario = models.PositiveIntegerField()
    categoria = models.CharField(
        max_length=50,
        choices=[
            ('Base', 'Pasta Base'),
            ('Derivado', 'Derivado'),
        ],
        default='Base'
    )

    def __str__(self):
        return self.nombre

# Modelo de Cliente
class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15)

    def __str__(self):
        return self.nombre

# Modelo de Pedido
class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    detalles = models.JSONField()  # Aquí se almacenan los detalles del pedido como JSON

    def __str__(self):
        return f"Pedido {self.id} - {self.cliente.nombre}"

# Modelo de Proveedor
class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.nombre

# Modelo de Envio
class Envio(models.Model):
    pedido = models.OneToOneField(Pedido, on_delete=models.CASCADE)
    direccion = models.TextField()
    ciudad = models.CharField(max_length=100)
    codigo_postal = models.CharField(max_length=10)
    estado = models.CharField(
        max_length=50,
        choices=[
            ('Pendiente', 'Pendiente'),
            ('En tránsito', 'En tránsito'),
            ('Entregado', 'Entregado'),
        ],
        default='Pendiente'
    )

    def __str__(self):
        return f"Envio {self.id} - {self.estado}"
