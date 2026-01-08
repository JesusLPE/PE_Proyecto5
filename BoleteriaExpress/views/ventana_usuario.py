import tkinter as tk
from tkinter import ttk
from utils.utilidades import cerrar_ventana, proximamente, mostrar_mensaje
from views.ventana_funciones import ventana_asientos  # Mantiene la selección de asientos existente

def ventana_usuario(root, nombre):
    root.withdraw()
    user_win = tk.Toplevel(root)
    user_win.title("Panel de Usuario - Boletería Express Ecuador")
    user_win.state("zoomed")
    user_win.configure(bg="white")
    user_win.resizable(True, True)

    # Header rojo
    header = tk.Frame(user_win, bg="#8B0000", height=100)
    header.pack(fill="x")
    header.pack_propagate(False)

    titulo = tk.Label(
        header, 
        text=f"¡Bienvenido {nombre}! 🚌 Boletería Express",
        fg="white", bg="#8B0000",
        font=("Segoe UI", 24, "bold")
    )
    titulo.pack(pady=25)

    # Buscador rápido de rutas
    buscador_frame = tk.Frame(user_win, bg="white")
    buscador_frame.pack(pady=30)

    tk.Label(buscador_frame, text="1. Buscador Rápido de Rutas", 
             font=("Segoe UI", 18, "bold"), bg="white", fg="#333333").pack()

    ruta_frame = tk.Frame(buscador_frame, bg="#f0f0f0", relief="groove", bd=2, padx=30, pady=20)
    ruta_frame.pack(pady=20)

    ciudades = ["N/A"]

    tk.Label(ruta_frame, text="Origen:", bg="#f0f0f0", font=("Segoe UI", 12)).grid(row=0, column=0, padx=15, pady=10)
    origen_cb = ttk.Combobox(ruta_frame, values=ciudades, state="readonly", width=15, font=("Segoe UI", 12))
    origen_cb.set("N/A")
    origen_cb.grid(row=0, column=1, padx=15, pady=10)

    tk.Label(ruta_frame, text="Destino:", bg="#f0f0f0", font=("Segoe UI", 12)).grid(row=0, column=2, padx=15, pady=10)
    destino_cb = ttk.Combobox(ruta_frame, values=ciudades, state="readonly", width=15, font=("Segoe UI", 12))
    destino_cb.set("N/A")
    destino_cb.grid(row=0, column=3, padx=15, pady=10)

    def buscar_ruta():
        if origen_cb.get() == "N/A" or destino_cb.get() == "N/A":
            proximamente("Buscar Rutas")
        elif origen_cb.get() == destino_cb.get():
            mostrar_mensaje("warning", "Advertencia", "Origen y destino deben ser diferentes")
        else:
            proximamente("Buscar Cooperativas")

    btn_buscar = tk.Button(ruta_frame, text="Buscar Cooperativas", bg="#8B0000", fg="white",
                           font=("Segoe UI", 14, "bold"), width=20, command=buscar_ruta)
    btn_buscar.grid(row=0, column=4, padx=30, pady=10)

    # Opciones rápidas
    opciones_frame = tk.Frame(user_win, bg="white")
    opciones_frame.pack(pady=40)

    tk.Label(opciones_frame, text="Opciones Rápidas de Boletería:",
             font=("Segoe UI", 18, "bold"), bg="white", fg="#8B0000").pack(pady=20)

    botones_frame = tk.Frame(opciones_frame, bg="white")
    botones_frame.pack()

    tk.Button(botones_frame, text="Mi Historial", width=20, height=2, bg="#8B0000", fg="white",
              font=("Segoe UI", 14, "bold"), command=lambda: proximamente("Mi Historial")).grid(row=0, column=0, padx=20, pady=10)

    tk.Button(botones_frame, text="Buscar por Horario", width=20, height=2, bg="#C71585", fg="white",
              font=("Segoe UI", 14, "bold"), command=lambda: proximamente("Buscar por Horario")).grid(row=0, column=1, padx=20, pady=10)

    tk.Button(botones_frame, text="Información", width=20, height=2, bg="#D2691E", fg="white",
          font=("Segoe UI", 14, "bold"),
          command=lambda: mostrar_mensaje(
              "info",
              "Información General",
              "Bienvenido a Boletería Express Ecuador\n\n"
              "Este es el portal para la compra y gestión de boletos interprovinciales en Ecuador.\n\n"
              "Aquí puedes:\n"
              "- Ingresar como usuario para comprar boletos y ver tu historial.\n"
              "- Registrarte si eres nuevo.\n"
              "- Acceder al panel de administrador si tienes credenciales autorizadas.\n\n"
              "Estamos trabajando en mejorar la experiencia para facilitar tus viajes."
          )).grid(row=0, column=2, padx=20, pady=10)
    
    tk.Button(botones_frame, text="Comprar Asiento", width=20, height=2, bg="#8B0000", fg="white",
              font=("Segoe UI", 14, "bold"), command=ventana_asientos).grid(row=0, column=3, padx=20, pady=10)

    # Botón Salir
    tk.Button(user_win, text="Salir", width=20, height=2, bg="#FF0000", fg="white",
              font=("Segoe UI", 14, "bold"), command=lambda: cerrar_ventana(user_win, root)).pack(pady=40)

    user_win.mainloop()