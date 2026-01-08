import tkinter as tk
from views.ventana_ver_usuarios import ver_usuarios
from views.ventana_funciones import ventana_asientos
from utils.utilidades import cerrar_ventana, proximamente, mostrar_mensaje

def ventana_admin(root, nombre):
    root.withdraw()
    win = tk.Toplevel(root)
    win.title("Panel del Administrador")
    win.state("zoomed")
    win.configure(bg="white")
    win.resizable(True, True)

    # Header rojo
    header = tk.Frame(win, bg="#8B0000", height=100)
    header.pack(fill="x")
    header.pack_propagate(False)

    titulo = tk.Label(
        header, 
        text=f"Panel Administrador - ¡Bienvenido {nombre}! 🚌 Boletería Express",
        fg="white", bg="#8B0000",
        font=("Segoe UI", 24, "bold")
    )
    titulo.pack(pady=25)

    # Opciones administrativas
    opciones_frame = tk.Frame(win, bg="white")
    opciones_frame.pack(expand=True, pady=60)

    tk.Label(opciones_frame, text="Funciones del Administrador",
             font=("Segoe UI", 20, "bold"), bg="white", fg="#8B0000").pack(pady=30)

    botones_frame = tk.Frame(opciones_frame, bg="white")
    botones_frame.pack()

    tk.Button(botones_frame, text="Vender Boletos\n(Seleccionar Asiento)", width=25, height=4, bg="#8B0000", fg="white",
              font=("Segoe UI", 14, "bold"), command=ventana_asientos).grid(row=0, column=0, padx=30, pady=20)

    tk.Button(botones_frame, text="Agregar Rutas", width=25, height=4, bg="#8B0000", fg="white",
              font=("Segoe UI", 14, "bold"), command=lambda: proximamente("Agregar Rutas")).grid(row=0, column=1, padx=30, pady=20)

    tk.Button(botones_frame, text="Ver Usuarios\nRegistrados", width=25, height=4, bg="#8B0000", fg="white",
              font=("Segoe UI", 14, "bold"), command=ver_usuarios).grid(row=1, column=0, padx=30, pady=20)

    tk.Button(botones_frame, text="Registro de Ventas", width=25, height=4, bg="#8B0000", fg="white",
              font=("Segoe UI", 14, "bold"), command=lambda: proximamente("Registro de Ventas")).grid(row=1, column=1, padx=30, pady=20)

    # Botón Salir
    tk.Button(win, text="Salir", width=20, height=2, bg="#FF0000", fg="white",
              font=("Segoe UI", 14, "bold"), command=lambda: cerrar_ventana(win, root)).pack(pady=50)