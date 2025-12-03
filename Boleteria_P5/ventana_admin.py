import tkinter as tk
from ventana_ver_usuarios import ver_usuarios
from ventana_funciones import ventana_funciones
from utilidades import cerrar_todo

def ventana_admin(root):
    win = tk.Toplevel()
    win.title("Panel del Administrador")
    win.geometry("600x600")
    win.resizable(False, False)

    tk.Label(win, text="PANEL DEL ADMINISTRADOR",
             font=("Segoe UI", 16, "bold")).pack(pady=20)

    tk.Button(
        win, text="Ver usuarios registrados",
        width=25, bg="#B22222", fg="white",
        font=("Segoe UI", 12, "bold"),
        command=ver_usuarios
    ).pack(pady=15)

    tk.Button(
        win, text="Funciones avanzadas",
        width=25, bg="#444444", fg="white",
        font=("Segoe UI", 12),
        command=ventana_funciones
    ).pack(pady=15)

    tk.Button(
        win, text="Salir",
        command=lambda: cerrar_todo(win, root)
    ).pack(pady=20)
