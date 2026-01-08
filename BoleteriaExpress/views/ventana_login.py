import tkinter as tk
from tkinter import messagebox
from data.usuarios import validar_usuario
from utils.utilidades import cerrar_ventana, mostrar_mensaje
from views.ventana_usuario import ventana_usuario
from views.ventana_admin import ventana_admin

def abrir_login(root):
    root.withdraw()
    login = tk.Toplevel(root)
    login.title("Iniciar Sesión")
    login.state("zoomed")
    login.resizable(True, True)
    login.configure(bg="white")

    # Header con fondo celeste claro
    header = tk.Frame(login, bg="#e6f7ff", height=100)
    header.pack(fill="x")

    # Título principal
    titulo = tk.Label(
        header, text="Iniciar Sesión",
        fg="#003366", bg="#e6f7ff",
        font=("Segoe UI", 24, "bold")
    )
    titulo.pack(pady=20)

    # Cuerpo principal centrado
    cuerpo = tk.Frame(login, bg="white")
    cuerpo.pack(expand=True, pady=20)

    tk.Label(cuerpo, text="Usuario:", bg="white", font=("Segoe UI", 12)).pack(pady=5)
    e_user = tk.Entry(cuerpo, width=30, font=("Segoe UI", 12))
    e_user.pack(pady=5)

    tk.Label(cuerpo, text="Contraseña:", bg="white", font=("Segoe UI", 12)).pack(pady=5)
    e_pass = tk.Entry(cuerpo, show="*", width=30, font=("Segoe UI", 12))
    e_pass.pack(pady=5)

    # ... (el resto del archivo permanece igual hasta validar_login)

    def validar_login():
        usuario = e_user.get()
        clave = e_pass.get()
        user_data = validar_usuario(usuario, clave)
        if user_data:
            cerrar_ventana(login)
            if usuario == "admin":
                ventana_admin(root, user_data["nombre"])
            else:
                ventana_usuario(root, user_data["nombre"])
        else:
            mostrar_mensaje("error", "Error", "Usuario o contraseña incorrectos")

    tk.Button(cuerpo, text="Ingresar", width=20,
              font=("Segoe UI", 14, "bold"), bg="#8B0000", fg="white",
              command=validar_login).pack(pady=20)

    tk.Button(cuerpo, text="Regresar", width=20,
              font=("Segoe UI", 14, "bold"), bg="#8B0000", fg="white",
              command=lambda: cerrar_ventana(login, root)).pack(pady=10)