import tkinter as tk
from tkinter import messagebox
from usuarios import usuarios
from ventana_usuario import ventana_usuario
from ventana_admin import ventana_admin
from utilidades import cerrar_ventana

def abrir_login(root):
    root.withdraw()
    login = tk.Toplevel()
    login.title("Iniciar Sesión")
    login.geometry("600x600")
    login.resizable(False, False)

    tk.Label(login, text="INICIAR SESIÓN",
             font=("Segoe UI", 16, "bold")).pack(pady=20)

    tk.Label(login, text="Usuario:").pack()
    e_user = tk.Entry(login)
    e_user.pack(pady=5)

    tk.Label(login, text="Contraseña:").pack()
    e_pass = tk.Entry(login, show="*")
    e_pass.pack(pady=5)

    def validar_login():
        usuario = e_user.get()
        clave = e_pass.get()

        for u in usuarios:
            if u["usuario"] == usuario and u["contraseña"] == clave:

                if usuario == "admin":
                    login.destroy()
                    ventana_admin(root)
                    return

                login.destroy()
                ventana_usuario(root)
                return

        messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    tk.Button(login, text="Ingresar", width=15,
              command=validar_login).pack(pady=10)

    tk.Button(login, text="Regresar", width=15,
              command=lambda: cerrar_ventana(login, root)).pack(pady=5)
