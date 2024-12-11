from django import forms
from .models import Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'inventario', 'categoria']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del Producto'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripción'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Precio'}),
            'inventario': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cantidad en Inventario'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),  # Menú desplegable para categorías
        }
    
    # Validación personalizada para el campo "precio"
    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        if precio <= 0:
            raise forms.ValidationError("El precio debe ser mayor a 0.")
        return precio

    # Validación personalizada para el campo "inventario"
    def clean_inventario(self):
        inventario = self.cleaned_data.get('inventario')
        if inventario < 0:
            raise forms.ValidationError("El inventario no puede ser negativo.")
        return inventario
