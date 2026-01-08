import tkinter as tk
from data.usuarios import agregar_usuario
from utils.utilidades import cerrar_ventana, mostrar_mensaje

def abrir_registro(root):
    root.withdraw()
    reg = tk.Toplevel(root)
    reg.title("Registro de Usuario")
    reg.state("zoomed")
    reg.resizable(True, True)
    reg.configure(bg="white")

    # Header con fondo celeste claro
    header = tk.Frame(reg, bg="#e6f7ff", height=100)
    header.pack(fill="x")

    # Título principal
    titulo = tk.Label(
        header, text="Registro de Usuario",
        fg="#003366", bg="#e6f7ff",
        font=("Segoe UI", 24, "bold")
    )
    titulo.pack(pady=20)

    # Cuerpo principal centrado
    cuerpo = tk.Frame(reg, bg="white")
    cuerpo.pack(expand=True, pady=20)

    tk.Label(cuerpo, text="Nombre:", bg="white", font=("Segoe UI", 12)).pack(pady=5)
    e_nombre = tk.Entry(cuerpo, width=30, font=("Segoe UI", 12))
    e_nombre.pack(pady=5)

    tk.Label(cuerpo, text="Usuario:", bg="white", font=("Segoe UI", 12)).pack(pady=5)
    e_usuario = tk.Entry(cuerpo, width=30, font=("Segoe UI", 12))
    e_usuario.pack(pady=5)

    tk.Label(cuerpo, text="Contraseña:", bg="white", font=("Segoe UI", 12)).pack(pady=5)
    e_pass = tk.Entry(cuerpo, show="*", width=30, font=("Segoe UI", 12))
    e_pass.pack(pady=5)

    def registrar_usuario():
        nombre = e_nombre.get()
        usuario = e_usuario.get()
        clave = e_pass.get()

        if not nombre or not usuario or not clave:
            mostrar_mensaje("warning", "Advertencia", "Todos los campos son obligatorios")
            return

        if agregar_usuario(nombre, usuario, clave):
            mostrar_mensaje("info", "Éxito", "Usuario registrado correctamente")
            cerrar_ventana(reg, root)
        else:
            mostrar_mensaje("error", "Error", "Ese usuario ya existe")

    tk.Button(reg, text="Registrar", width=20,
              font=("Segoe UI", 14, "bold"), bg="#8B0000", fg="white",
              command=registrar_usuario).pack(pady=20)

    tk.Button(reg, text="Regresar", width=20,
              font=("Segoe UI", 14, "bold"), bg="#8B0000", fg="white",
              command=lambda: cerrar_ventana(reg, root)).pack(pady=10)