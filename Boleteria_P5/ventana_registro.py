import tkinter as tk
from tkinter import messagebox
from usuarios import usuarios
from utilidades import cerrar_ventana

def abrir_registro(root):
    root.withdraw()
    reg = tk.Toplevel()
    reg.title("Registro de Usuario")
    reg.geometry("600x600")
    reg.resizable(False, False)

    tk.Label(reg, text="REGISTRO DE USUARIO",
             font=("Segoe UI", 16, "bold")).pack(pady=20)

    tk.Label(reg, text="Nombre:").pack()
    e_nombre = tk.Entry(reg)
    e_nombre.pack(pady=5)

    tk.Label(reg, text="Usuario:").pack()
    e_usuario = tk.Entry(reg)
    e_usuario.pack(pady=5)

    tk.Label(reg, text="Contraseña:").pack()
    e_pass = tk.Entry(reg, show="*")
    e_pass.pack(pady=5)

    def registrar_usuario():
        nombre = e_nombre.get()
        usuario = e_usuario.get()
        clave = e_pass.get()

        if nombre == "" or usuario == "" or clave == "":
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios")
            return

        for u in usuarios:
            if u["usuario"] == usuario:
                messagebox.showerror("Error", "Ese usuario ya existe")
                return

        usuarios.append({"nombre": nombre, "usuario": usuario, "contraseña": clave})

        messagebox.showinfo("Éxito", "Usuario registrado correctamente")
        cerrar_ventana(reg, root)

    tk.Button(reg, text="Registrar", width=15,
              command=registrar_usuario).pack(pady=10)

    tk.Button(reg, text="Regresar", width=15,
              command=lambda: cerrar_ventana(reg, root)).pack(pady=5)
