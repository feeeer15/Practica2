import tkinter as tk
from back import *
from tkinter import messagebox 
from PIL import Image, ImageTk

cliente_actual = None
empleado_actual = None


def ventana_de_inicio():
    global root
    root = tk.Tk()
    root.title("Inicio de sesión")
    root.geometry("600x600")
    root.config(bg="#372414")
    root.iconbitmap("C://Users//maxim//OneDrive//Escritorio//mafer´s folder//inicio.ico")

    titulo = tk.Label(root, text=f"Bienvenido!", font=("GLANCE", 60 ), fg="#B7A087", bg="#372414", padx=20, pady=100)
    titulo.pack()

    global entrada1, entrada2
    etiqueta1 = tk.Label(root, text="Usuario:", fg="#B7A087", bg="#372414", font=("Century Gothic", 20))
    entrada1 = tk.Entry(root, fg="#372414", bg="#B7A087", font=("Century Gothic", 15))
    etiqueta2 = tk.Label(root, text="Contraseña:", fg="#B7A087", bg="#372414", font=("Century Gothic", 20))
    entrada2 = tk.Entry(root, fg="#372414", bg="#B7A087", font=("Century Gothic", 15), show="★")  

    etiqueta1.pack()
    entrada1.pack()
    etiqueta2.pack()
    entrada2.pack()

    boton_login = tk.Button(root, text="Iniciar Sesión", fg="#372414", bg="#B7A087", font=("Century Gothic", 15), command=inicio)
    boton_login.pack(pady=20)
    root.protocol("WM_DELETE_WINDOW", al_cerrar)
    root.mainloop()

def al_cerrar():
    root.destroy()

def inicio():
    global cliente_actual, empleado_actual
    usuario = entrada1.get()
    password = entrada2.get()
    usuario_iniciar = Usuario.iniciar_sesion(usuario, password)

    if usuario_iniciar is not None and hasattr(usuario_iniciar, "rol"):
        root.destroy()
        if usuario_iniciar.rol == "Empleado":
            empleado_actual = usuario_iniciar.persona
            ventana_empleado()
        elif usuario_iniciar.rol == "Cliente":
            cliente_actual = usuario_iniciar.persona
            ventana_cliente()
        else:
            messagebox.showerror("Error", "Rol desconocido")
    else:
        messagebox.showerror("Error de inicio de sesión", "Usuario o contraseña incorrectos. Intente de nuevo")

def ventana_empleado():
    root2 = tk.Tk()
    root2.title("Ventana Empleado")
    root2.geometry("600x600")
    root2.config(bg="#4F483F")
    root2.iconbitmap("C://Users//maxim//OneDrive//Escritorio//mafer´s folder//empleado.ico")

    Letrero = tk.Label(root2, text="Panel de Empleados", font=("GLANCE", 40 ), fg="#B7A087", bg="#4F483F", padx=20, pady=30)
    Letrero.pack()

    imagen5 = Image.open("C://Users//maxim//OneDrive//Escritorio//mafer´s folder//cocinero.jpeg")
    imagen5 = imagen5.resize((250, 250))
    imagen2_tk = ImageTk.PhotoImage(imagen5)
    label_imagen = tk.Label(root2, image=imagen2_tk, bg="#4F483F")
    label_imagen.image = imagen2_tk
    label_imagen.place(relx=1.0, rely=1.0, anchor="se")

    tk.Button(root2, text="★ Ver inventario", fg="#4F483F", bg="#B7A087", font=("Century Gothic", 15), command=ver_inventario).pack(pady=20)
    tk.Button(root2, text="★ Actualizar inventario", fg="#4F483F", bg="#B7A087", font=("Century Gothic", 15), command=actualizar_inventario).pack(pady=20)
    tk.Button(root2, text="Cerrar sesión", fg="#4F483F", bg="#B7A087", font=("Century Gothic", 15), command=lambda:cerrar_sesion(root2)).pack(pady=45)

def ventana_cliente():
    root3 = tk.Tk()
    root3.title("Ventana Cliente")
    root3.geometry("600x600")
    root3.config(bg="#3D0A05")
    root3.iconbitmap("C://Users//maxim//OneDrive//Escritorio//mafer´s folder//cliente.ico")

    imagen = Image.open("C://Users//maxim//OneDrive//Escritorio//mafer´s folder//esnupi.jpeg")
    imagen = imagen.resize((200, 200))
    imagen_tk = ImageTk.PhotoImage(imagen)
    label_imagen = tk.Label(root3, image=imagen_tk, bg="#3D0A05")
    label_imagen.image = imagen_tk
    label_imagen.place(relx=1.0, rely=1.0, anchor="se")

    bienvenida = tk.Label(root3, text="Bienvenido", font=("GLANCE", 50), fg="#B5977F", bg="#3D0A05", padx=20, pady=30)
    bienvenida.pack()

    tk.Button(root3, text="★ Realizar nuevo pedido", fg="#3D0A05", bg="#B5977F", font=("Century Gothic", 15), command=realizar_pedido).pack(pady=20)
    tk.Button(root3, text="★ Revisar historial de compras", fg="#3D0A05", bg="#B5977F", font=("Century Gothic", 15), command=revisar_historial).pack(pady=15)
    tk.Button(root3, text="★ Cancelar pedido", fg="#3D0A05", bg="#B5977F", font=("Century Gothic", 15), command=cancelar_pedido).pack(pady=15)
    tk.Button(root3, text="Cerrar sesión", fg="#3D0A05", bg="#B5977F", font=("Century Gothic", 15), command=lambda:cerrar_sesion(root3)).pack(pady=45)
    root3.mainloop()

def ver_inventario():
    root7 = tk.Tk()
    root7.title("Inventario actual")
    root7.geometry("600x600")
    root7.iconbitmap("C://Users//maxim//OneDrive//Escritorio//mafer´s folder//inventario.ico")
    root7.config(bg="#2C0001")

    Titulo = tk.Label(root7, text="Inventario", font=("GLANCE", 45), fg="#837a75", bg="#2C0001", padx=20, pady=30)
    Titulo.pack()

    stock = inventario.consultar_inventario()

    if not stock:
        tk.Label(root7, text="No hay artículos en el inventario", font=("Century Gothic", 16), fg="#B7A087", bg="#2C0001").pack()
    else:
        listbox = tk.Listbox(root7, bg="#2C0001", fg="#837a75", font=("Century Gothic", 16))
        listbox.pack(fill=tk.BOTH, expand=True)

        for ingrediente, cantidad in stock.items():
            listbox.insert(tk.END, f"★ {ingrediente}: {cantidad} unidades")



def actualizar_inventario():
    ventana = tk.Tk()
    ventana.title("Actualizar inventario")
    ventana.geometry("400x300")
    ventana.config(bg="#837a75")
    ventana.iconbitmap("C://Users//maxim//OneDrive//Escritorio//mafer´s folder//inventario.ico")

    marco = tk.Frame(ventana, bg="#837a75")
    marco.place(relx=0.5, rely=0.5, anchor="center") 

    tk.Label(marco, text="Ingrediente:", font=("Century Gothic", 18), fg="#2C0001", bg="#837a75").pack(pady=(0, 5))
    entrada_ing = tk.Entry(marco, fg="#837a75", bg="#2C0001", font=("Century Gothic", 15))
    entrada_ing.pack(pady=(0, 20))

    tk.Label(marco, text="Cantidad:", font=("Century Gothic", 18), fg="#2C0001", bg="#837a75").pack(pady=(0, 5))
    entrada_cant = tk.Entry(marco, fg="#837a75", bg="#2C0001", font=("Century Gothic", 15))
    entrada_cant.pack(pady=(0, 20))

    def actualizar():
        ing = entrada_ing.get()
        try:
            cant = int(entrada_cant.get())
            empleado1.actualizar_inventario(inventario, ing, cant)
            messagebox.showinfo("Éxito", f"{cant} unidades de {ing} añadidas.")
            ventana.destroy()
        except ValueError:
            messagebox.showerror("Error", "Cantidad inválida")

    tk.Button(marco, text="Actualizar", font=("Century Gothic", 12), fg="#837a75", bg="#2C0001", command=actualizar).pack()

def realizar_pedido():
    root4 = tk.Toplevel()
    root4.title("Realizar pedido")
    root4.geometry("600x600")
    root4.config(bg="#26170F")
    root4.iconbitmap("C://Users//maxim//OneDrive//Escritorio//mafer´s folder//pedido.ico")

    imagen2 = Image.open("C://Users//maxim//OneDrive//Escritorio//mafer´s folder//cafee.jpeg")
    imagen2 = imagen2.resize((200, 200))
    imagen2_tk = ImageTk.PhotoImage(imagen2)
    label_imagen = tk.Label(root4, image=imagen2_tk, bg="#26170F")
    label_imagen.image = imagen2_tk
    label_imagen.place(relx=1.0, rely=1.0, anchor="se")

    Compra = tk.Label(root4, text="Comienza tu orden", font=("GLANCE", 40), fg="#B7A087", bg="#26170F", padx=20, pady=30)
    Compra.pack()

    Nota = tk.Label(root4, text="Nota: Ten en cuenta que al hacer click en el producto\nautomaticamente se agrega al pedido", font=("Century Gothic", 14), fg="#B7A087", bg="#26170F")
    Nota.pack()

    pedido = Pedido(cliente_actual)

    def agregar_producto(index):
        pedido.agregar_producto(productos[index])

    frame_botones = tk.Frame(root4, bg="#26170F")
    frame_botones.pack(pady=10)  

    botones_por_fila = 3

    for i, prod in enumerate(productos):
        fila = i // botones_por_fila
        columna = i % botones_por_fila
        tk.Button(
            frame_botones,
            text=f"{prod.nombre} - ${prod.precio}",
            font=("Century Gothic", 15),
            fg="#26170F",
            bg="#B7A087",
            width=15,
            command=lambda i=i: agregar_producto(i)
        ).grid(row=fila, column=columna, padx=5, pady=5)

    def confirmar():
        cliente_actual.realizar_pedido(pedido, inventario)
        messagebox.showinfo("Pedido realizado", f"Total: ${pedido.calcular_total()}")
        root4.destroy()

    tk.Button(root4, text="Confirmar pedido", font=("Century Gothic", 15), fg="#26170F", bg="#B7A087", command=confirmar).pack(pady=100)


def revisar_historial():
    root5 = tk.Toplevel()
    root5.title("Revisar historial")
    root5.geometry("600x600")
    root5.config(bg="#4B0101")
    root5.iconbitmap("C://Users//maxim//OneDrive//Escritorio//mafer´s folder//historial.ico")

    tk.Label(root5, text="Historial de compras", font=("GLANCE", 35), fg="#F5F5DC", bg="#4B0101", padx=20, pady=30).pack()

    imagen3 = Image.open("C://Users//maxim//OneDrive//Escritorio//mafer´s folder//snopyyy.jpeg")
    imagen3 = imagen3.resize((200, 200))
    imagen3_tk = ImageTk.PhotoImage(imagen3)
    label_imagen = tk.Label(root5, image=imagen3_tk, bg="#4B0101")
    label_imagen.image = imagen3_tk
    label_imagen.place(relx=1.0, rely=1.0, anchor="se")

    for i, pedido in enumerate(cliente_actual.historial_pedidos, start=1):
        detalle = f"Pedido {i}: Total: ${pedido.calcular_total()} - Estado: {pedido.estado}"
        tk.Label(root5, text=detalle, font=("Century Gothic", 15), fg="#F5F5DC", bg="#4B0101").pack(pady=5)
        

def cancelar_pedido():
    root6 = tk.Toplevel()
    root6.title("Cancelar pedido")
    root6.geometry("600x600")
    root6.config(bg="#000000")
    root6.iconbitmap("C://Users//maxim//OneDrive//Escritorio//mafer´s folder//cancelar.ico")

    imagen4 = Image.open("C://Users//maxim//OneDrive//Escritorio//mafer´s folder//esnupitriste.jpeg")
    imagen4 = imagen4.resize((200, 200))
    imagen4_tk = ImageTk.PhotoImage(imagen4)
    label_imagen = tk.Label(root6, image=imagen4_tk, bg="#000000")
    label_imagen.image = imagen4_tk
    label_imagen.place(relx=1.0, rely=1.0, anchor="se")

    tk.Label(root6, text="Cancelación de pedido", font=("GLANCE", 35), fg="#F5F5DC", bg="#000000", padx=20, pady=30).pack()

    pedidos_activos = [p for p in cliente_actual.historial_pedidos if p.estado != "Cancelado"]
    listbox = tk.Listbox(root6, font=("Century Gothic", 15), bg="#000000", fg="#F5F5DC", width=50)
    for i, pedido in enumerate(pedidos_activos):
        listbox.insert(tk.END, f"Pedido {i+1}: ${pedido.calcular_total()} - {pedido.estado}")
    listbox.pack()

    def cancelar():
        i = listbox.curselection()
        if i:
            pedido = pedidos_activos[i[0]]
            pedido.actualizar_estado("Cancelado")
            cliente_actual.guardar_historial() 
            messagebox.showinfo("Cancelado", "Pedido cancelado correctamente")
            root6.destroy()

    tk.Button(root6, text="Cancelar", command=cancelar, font=("Century Gothic", 15), bg="#F5F5DC", fg="#000000").pack()
    root6.mainloop()

def cerrar_sesion(ventana_actual):
    ventana_actual.destroy() 
    ventana_de_inicio() 


ventana_de_inicio()
