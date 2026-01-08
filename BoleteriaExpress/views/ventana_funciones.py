import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from utils.utilidades import mostrar_mensaje

# Matriz de asientos del bus (13 filas x 4 columnas: A, B, C, D)
bus = [[f"{chr(65 + j)}{i}" for j in range(4)] for i in range(1, 14)]

def ventana_asientos():
    asi = tk.Toplevel()
    asi.title("Seleccionar asiento")
    asi.geometry("600x800")  # Ajustado para más filas
    asi.resizable(False, False)
    asi.configure(bg="#f0f0f0")

    tk.Label(asi, text="SELECCIONA TU ASIENTO",
             font=("Segoe UI", 14, "bold"), bg="#f0f0f0").pack(pady=10)

    # Contenedor principal (el cuerpo del bus)
    frame_bus = tk.Frame(asi, bg="#e0e0e0", padx=20, pady=20, highlightbackground="#555", highlightthickness=2, relief="groove")
    frame_bus.pack(pady=20, padx=20)

    # --- ZONA FRONTAL (Fila 0) ---
    # Asiento naranja izquierda (decorativo, no clickeable)
    tk.Label(frame_bus, width=6, height=2, bg="#f39c12", relief="raised").grid(row=0, column=0, padx=5, pady=5)
   
    # Dummy label para alinear columna 1 (invisible)
    tk.Label(frame_bus, width=6, height=2, bg="#e0e0e0").grid(row=0, column=1, padx=5, pady=5)
   
    # Espacio vacío (pasillo, más ancho para simetría)
    tk.Label(frame_bus, width=6, bg="#e0e0e0").grid(row=0, column=2)
   
    # Cabina conductor (Fondo negro con asiento naranja, decorativo)
    cabina = tk.Frame(frame_bus, bg="#222", padx=10, pady=5, relief="raised")
    cabina.grid(row=0, column=3, columnspan=2, sticky="nsew")
    tk.Label(cabina, width=12, height=2, bg="#f39c12", relief="raised").pack()  # Ancho doble para cubrir dos columnas

    # --- FILAS DE PASAJEROS (13 filas) ---
    for fila in range(1, 14):
        i = fila - 1  # Índice en la matriz bus

        # Asientos izquierda (Columna A y B)
        btnA = tk.Button(frame_bus, text=bus[i][0], width=6, height=2, bg="#27ae60", activebackground="#229954",
                         font=("Segoe UI", 10, "bold"), fg="white", relief="raised")
        btnA.grid(row=fila, column=0, padx=5, pady=5)
        btnA.config(command=lambda i=i, j=0, b=btnA: ocupar_asiento(i, j, b))

        btnB = tk.Button(frame_bus, text=bus[i][1], width=6, height=2, bg="#27ae60", activebackground="#229954",
                         font=("Segoe UI", 10, "bold"), fg="white", relief="raised")
        btnB.grid(row=fila, column=1, padx=5, pady=5)
        btnB.config(command=lambda i=i, j=1, b=btnB: ocupar_asiento(i, j, b))

        # Pasillo central (Columna 2, más ancho)
        tk.Label(frame_bus, width=6, bg="#e0e0e0").grid(row=fila, column=2)

        # Asientos derecha (Columna C y D)
        btnC = tk.Button(frame_bus, text=bus[i][2], width=6, height=2, bg="#27ae60", activebackground="#229954",
                         font=("Segoe UI", 10, "bold"), fg="white", relief="raised")
        btnC.grid(row=fila, column=3, padx=5, pady=5)
        btnC.config(command=lambda i=i, j=2, b=btnC: ocupar_asiento(i, j, b))

        btnD = tk.Button(frame_bus, text=bus[i][3], width=6, height=2, bg="#27ae60", activebackground="#229954",
                         font=("Segoe UI", 10, "bold"), fg="white", relief="raised")
        btnD.grid(row=fila, column=4, padx=5, pady=5)
        btnD.config(command=lambda i=i, j=3, b=btnD: ocupar_asiento(i, j, b))

    # Botón para cerrar la ventana
    tk.Button(asi, text="Cerrar", command=asi.destroy, width=20, font=("Segoe UI", 12), bg="#B22222", fg="white").pack(pady=20)

def ocupar_asiento(i, j, boton):
    asiento = bus[i][j]
    if asiento == "Ocupado":
        mostrar_mensaje("info", "Aviso", "Ese asiento ya está ocupado.")
        return
    
    # Diálogo de confirmación para comprar
    confirmar = messagebox.askyesno("Confirmar Compra", f"¿Desea comprar el asiento {asiento}?")
    if confirmar:
        bus[i][j] = "Ocupado"
        boton.config(text="Ocupado", bg="red", fg="white")
        messagebox.showinfo("Éxito", f"Asiento {asiento} comprado exitosamente.")
    # Si no confirma, no hace nada

def ventana_funciones():
    win = tk.Toplevel()
    win.title("Funciones avanzadas")
    win.geometry("500x500")
    win.resizable(False, False)

    # Cargar logo
    try:
        ruta_logo = "assets/logodlaya.jpg"
        img_pil = Image.open(ruta_logo).resize((500, 500))
        logo_tk = ImageTk.PhotoImage(img_pil)
        label_logo = tk.Label(win, image=logo_tk)
        label_logo.pack(pady=10)
        label_logo.image = logo_tk  # Referencia para evitar garbage collection
    except Exception as e:
        tk.Label(win, text="[Error al cargar logo]", fg="red").pack(pady=10)

    tk.Label(win, text="FUNCIONES AVANZADAS",
             font=("Segoe UI", 16, "bold")).pack(pady=20)

    tk.Button(win, text="Seleccionar Asiento",
              font=("Segoe UI", 12),
              width=20,
              command=ventana_asientos).pack(pady=15)