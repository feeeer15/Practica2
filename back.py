import json
import os


class ProductoBase:
    def __init__(self, nombre, precio):
        self.nombre = nombre
        self.precio = precio
        self.ingredientes = {}

class Bebida(ProductoBase):
    def __init__(self, nombre, precio, tamaño, tipo, personalizacion={}):
        super().__init__(nombre, precio)
        self.tamaño = tamaño
        self.tipo = tipo
        self.personalizacion = personalizacion
        self.ingredientes = {"Agua": 1}
        self.ingredientes.update(personalizacion)

    def descripcion(self):
        print(f" ☆ Nombre: {self.nombre}")
        print(f" ☆ Precio: ${self.precio}")
        print(f" ☆ Tamaño: {self.tamaño}")
        print("Ingredientes:")
        for ingrediente in self.ingredientes:
            print(f"- {ingrediente}")

class Postre(ProductoBase):
    def __init__(self, nombre, precio, personalizacion={}, vegano=False, sin_gluten=False):
        super().__init__(nombre, precio)
        self.vegano = vegano
        self.sin_gluten = sin_gluten
        self.personalizacion = personalizacion
        self.ingredientes = {"Harina": 1}
        self.ingredientes.update(personalizacion)

    def descripcion(self):
        print(f" ☆ Nombre: {self.nombre}")
        print(f" ☆ Precio: ${self.precio}")
        print(f" ☆ Vegano: {'Sí' if self.vegano else 'No'}")
        print(f" ☆ Sin gluten: {'Sí' if self.sin_gluten else 'No'}")
        print("Ingredientes:")
        for ingrediente in self.ingredientes:
            print(f"- {ingrediente}")

# ==============================
# Productos disponibles
# ==============================

bebida1 = Bebida("Latte", 45, "Grande", "Caliente", {"Café": 1, "Leche": 2})
bebida2 = Bebida("Capuccino", 50, "Mediano", "Caliente", {"Café": 1, "Leche": 1})
bebida3 = Bebida("Té Verde", 35, "Chico", "Frío", {"Té Verde": 1})
bebida4 = Bebida("Expresso", 35, "Chico", "Frío", {"Café": 2})

postre1 = Postre("Brownie", 30, {}, vegano=False, sin_gluten=False)
postre2 = Postre("Galleta", 20, {}, vegano=True)
postre3 = Postre("Panqué", 25, {}, vegano=False, sin_gluten=True)
postre4 = Postre("Afogatto", 70, {}, vegano=False)

productos = [bebida1, bebida2, bebida3, bebida4, postre1, postre2, postre3, postre4]

# ==============================
# Clases principales
# ==============================

class Usuario:
    lista_usuario = []

    def __init__(self, Nombre, Rol, Password, Persona):
        self.nombre = Nombre
        self.rol = Rol
        self.__pass = Password
        self.persona = Persona
        Usuario.lista_usuario.append(self)

    def info(self):
        return f"El usuario se llama {self.nombre}, tiene rol de {self.rol}"

    @classmethod
    def iniciar_sesion(cls, nombre, password):
        for usuario in Usuario.lista_usuario:
            if usuario.nombre == nombre and usuario._Usuario__pass == password:
                print(f"Bienvenido/a {usuario.nombre}, acabas de iniciar sesión")
                return usuario
        print("Datos incorrectos para inicio de sesión")
        return None

class Cliente:
    def __init__(self, nombre, rol):
        self.nombre = nombre
        self.rol = rol
        self.historial_pedidos = []
        self.puntos_lealtad = 0
        self.cargar_historial()

    def realizar_pedido(self, pedido, inventario, promocion=None):
        if pedido.verificar_disponibilidad(inventario):
            if promocion and self.puntos_lealtad >= 50:
                promocion.aplicar_descuento(pedido)
            self.historial_pedidos.append(pedido)
            self.puntos_lealtad += 10
            pedido.actualizar_stock(inventario)
            pedido.actualizar_estado("En preparación")
            print("Productos:")
            for producto in pedido.productos:
                print(f"- {producto.nombre}: ${producto.precio}")
            print(f"Total con descuento: ${pedido.calcular_total()}")
            self.guardar_historial()
        else:
            print("El pedido no puede ser realizado ya que no hay los insumos suficientes")

    def consultar_historial(self):
        print(f"Historial pedidos de {self.nombre}")
        for pedido in self.historial_pedidos:
            print(f"Pedido con total: ${pedido.calcular_total()} - Estado: {pedido.estado}")

    def guardar_historial(self):
        historial = []
        for pedido in self.historial_pedidos:
            pedido_data = {
                'productos': [{'nombre': p.nombre, 'precio': p.precio} for p in pedido.productos],
                'total': pedido.calcular_total(),
                'estado': pedido.estado
            }
            historial.append(pedido_data)
        with open(f"{self.nombre}_historial.json", "w") as f:
            json.dump(historial, f, indent=4)

    def cargar_historial(self):
        try:
            with open(f"{self.nombre}_historial.json", "r") as f:
                historial = json.load(f)
                for pedido_data in historial:
                    pedido = Pedido(self)
                    for producto_data in pedido_data['productos']:
                        for prod in productos:
                            if prod.nombre == producto_data['nombre']:
                                pedido.agregar_producto(prod)
                    pedido.estado = pedido_data['estado']
                    self.historial_pedidos.append(pedido)
        except FileNotFoundError:
            self.historial_pedidos = []

class Empleado:
    def __init__(self, nombre, rol):
        self.nombre = nombre
        self.rol = rol

    def actualizar_inventario(self, inventario, ingrediente, cantidad):
        inventario.agregar_articulo(ingrediente, cantidad)
        print(f"Se han añadido {cantidad} unidades de {ingrediente}")

class Inventario:
    def __init__(self):
        self.stock = {}
        self.ruta_archivo = "inventario.json"
        self.cargar_desde_archivo()

    def agregar_articulo(self, ingrediente, cantidad):
        self.stock[ingrediente] = self.stock.get(ingrediente, 0) + cantidad
        self.guardar_en_archivo()

    def verificar_disponibilidad(self, ingredientes):
        faltantes = [ing for ing, cantidad in ingredientes.items() if self.stock.get(ing, 0) < cantidad]
        if faltantes:
            print(f" ☆ Faltan ingredientes: {', '.join(faltantes)}")
            return False
        return True

    def actualizar_stock(self, ingredientes):
        for ing, cantidad in ingredientes.items():
            if ing in self.stock:
                self.stock[ing] -= cantidad
        self.guardar_en_archivo()

    def guardar_en_archivo(self):
        with open(self.ruta_archivo, "w") as f:
            json.dump(self.stock, f)

    def cargar_desde_archivo(self):
        if os.path.exists(self.ruta_archivo):
            with open(self.ruta_archivo, "r") as f:
                self.stock = json.load(f)

    def consultar_inventario(self):
        print("Inventario actual:")
        for ing, cantidad in self.stock.items():
            print(f"☆ {ing}: {cantidad} unidades")
        return self.stock

class Pedido:
    def __init__(self, cliente):
        self.cliente = cliente
        self.productos = []
        self.estado = "Pendiente"
        self.total = 0
        print(f" ☆ Se ha añadido un nuevo pedido para {self.cliente.nombre}")

    def agregar_producto(self, producto):
        self.productos.append(producto)
        self.total += producto.precio
        print(f" ☆ Se ha añadido {producto.nombre} con costo de ${producto.precio} al pedido de {self.cliente.nombre}")

    def calcular_total(self):
        return self.total

    def actualizar_estado(self, nuevo_estado):
        self.estado = nuevo_estado
        print(f" ☆ Nuevo estado del pedido: {self.estado}")

    def verificar_disponibilidad(self, inventario):
        return all(inventario.verificar_disponibilidad(prod.ingredientes) for prod in self.productos)

    def actualizar_stock(self, inventario):
        for prod in self.productos:
            inventario.actualizar_stock(prod.ingredientes)

class Promocion:
    def __init__(self, descripcion, descuento):
        self.descripcion = descripcion
        self.descuento = descuento

    def aplicar_descuento(self, pedido):
        pedido.total *= (1 - self.descuento / 100)


inventario = Inventario()

cliente1 = Cliente("feeer", "Cliente")
usuario_cliente1 = Usuario("feeer", "Cliente", "1234", cliente1)

empleado1 = Empleado("Mafer", "Empleado")
usuario_empleado1 = Usuario("Mafer", "Empleado", "1234", empleado1)