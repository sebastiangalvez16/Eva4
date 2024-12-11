import requests

BASE_URL = "http://127.0.0.1:8000/api/productos/"  # URL base de la API
LOGIN_URL = "http://127.0.0.1:8000/login/"  # URL para login
REGISTER_URL = "http://127.0.0.1:8000/register/"  # URL para registro

# Variable global para almacenar el token de autenticación
AUTH_HEADERS = {}

def login():
    """Función para iniciar sesión y obtener el token JWT"""
    global AUTH_HEADERS
    print("\n--- Iniciar Sesión ---")
    username = input("Usuario: ")
    password = input("Contraseña: ")
    response = requests.post(LOGIN_URL, data={"username": username, "password": password})
    try:
        if response.status_code == 200:
            print("Inicio de sesión exitoso.")
            data = response.json()
            token = data.get("access")  # Usar el token de acceso
            AUTH_HEADERS = {"Authorization": f"Bearer {token}"}
        else:
            error_message = response.json().get("error", "Credenciales incorrectas.")
            print("Error al iniciar sesión:", error_message)
    except requests.exceptions.JSONDecodeError:
        print("Error al iniciar sesión: Respuesta inesperada del servidor.")

def register():
    """Función para registrar un nuevo usuario"""
    print("\n--- Registrarse ---")
    username = input("Usuario: ")
    password = input("Contraseña: ")
    email = input("Correo Electrónico (opcional): ")
    response = requests.post(REGISTER_URL, data={"username": username, "password": password, "email": email})
    try:
        if response.status_code == 201:
            print("Usuario registrado exitosamente. Ahora puedes iniciar sesión.")
        else:
            error_message = response.json().get("error", "Error desconocido.")
            print("Error al registrarse:", error_message)
    except requests.exceptions.JSONDecodeError:
        print("Error al registrarse: Respuesta inesperada del servidor.")

def mostrar_menu():
    """Mostrar menú principal"""
    print("\n--- Gestión de Productos ---")
    print("1. Crear Producto")
    print("2. Listar Productos")
    print("3. Actualizar Producto")
    print("4. Eliminar Producto")
    print("5. Salir")

def crear_producto():
    """Función para crear un producto"""
    print("\n--- Crear Producto ---")
    nombre = input("Nombre: ")
    descripcion = input("Descripción: ")
    precio = input("Precio: ")
    inventario = input("Inventario: ")
    categoria = input("Categoría (Base o Derivado): ")
    producto = {
        "nombre": nombre,
        "descripcion": descripcion,
        "precio": precio,
        "inventario": inventario,
        "categoria": categoria,
    }
    response = requests.post(BASE_URL, json=producto, headers=AUTH_HEADERS)
    if response.status_code == 201:
        print("Producto creado exitosamente.")
    else:
        try:
            error_message = response.json()
        except requests.exceptions.JSONDecodeError:
            error_message = "Respuesta inesperada del servidor."
        print("Error al crear el producto:", error_message)

def listar_productos():
    """Función para listar productos"""
    print("\n--- Lista de Productos ---")
    response = requests.get(BASE_URL, headers=AUTH_HEADERS)
    if response.status_code == 200:
        productos = response.json()
        if productos:
            for producto in productos:
                print(f"ID: {producto['id']}, Nombre: {producto['nombre']}, Categoría: {producto['categoria']}, Precio: ${producto['precio']}")
        else:
            print("No hay productos disponibles.")
    else:
        print("Error al obtener los productos:", response.text)

def actualizar_producto():
    """Función para actualizar un producto"""
    print("\n--- Actualizar Producto ---")
    producto_id = input("ID del Producto a actualizar: ")
    response = requests.get(f"{BASE_URL}{producto_id}/", headers=AUTH_HEADERS)

    # Verificar si el producto existe
    if response.status_code == 200:
        try:
            producto = response.json()
            print("Deja el campo vacío para mantener el valor actual.")
            nombre = input(f"Nombre [{producto['nombre']}]: ") or producto['nombre']
            descripcion = input(f"Descripción [{producto['descripcion']}]: ") or producto['descripcion']
            precio = input(f"Precio [{producto['precio']}]: ") or producto['precio']
            inventario = input(f"Inventario [{producto['inventario']}]: ") or producto['inventario']
            categoria = input(f"Categoría [{producto['categoria']}]: ") or producto['categoria']
            producto_actualizado = {
                "nombre": nombre,
                "descripcion": descripcion,
                "precio": precio,
                "inventario": inventario,
                "categoria": categoria,
            }
            update_response = requests.put(f"{BASE_URL}{producto_id}/", json=producto_actualizado, headers=AUTH_HEADERS)
            if update_response.status_code == 200:
                print("Producto actualizado exitosamente.")
            else:
                print("Error al actualizar el producto:", update_response.json())
        except requests.exceptions.JSONDecodeError:
            print("Error al obtener detalles del producto: Respuesta inesperada del servidor.")
    elif response.status_code == 404:
        print(f"Producto con ID {producto_id} no encontrado.")
    else:
        print(f"Error al obtener detalles del producto. Código de estado: {response.status_code}, Respuesta: {response.text}")

def eliminar_producto():
    """Función para eliminar un producto"""
    print("\n--- Eliminar Producto ---")
    producto_id = input("ID del Producto a eliminar: ")
    response = requests.delete(f"{BASE_URL}{producto_id}/", headers=AUTH_HEADERS)
    if response.status_code == 204:
        print("Producto eliminado exitosamente.")
    else:
        print(f"Error al eliminar el producto. Código de estado: {response.status_code}, Respuesta: {response.text}")

def main():
    """Función principal"""
    print("--- Bienvenido a la Gestión de Productos ---")
    while True:
        print("\n1. Iniciar Sesión")
        print("2. Registrarse")
        print("3. Salir")
        opcion = input("Selecciona una opción: ")
        if opcion == "1":
            login()
            if AUTH_HEADERS:
                break
        elif opcion == "2":
            register()
        elif opcion == "3":
            print("Saliendo del programa...")
            return
        else:
            print("Opción no válida. Intenta de nuevo.")

    while True:
        mostrar_menu()
        opcion = input("Selecciona una opción: ")
        if opcion == "1":
            crear_producto()
        elif opcion == "2":
            listar_productos()
        elif opcion == "3":
            actualizar_producto()
        elif opcion == "4":
            eliminar_producto()
        elif opcion == "5":
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    main()
