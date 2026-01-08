import tkinter as tk
from data.usuarios import obtener_todos_usuarios

def ver_usuarios():
    win = tk.Toplevel()
    win.title("Usuarios Registrados")
    win.geometry("500x500")
    win.resizable(False, False)

    tk.Label(win, text="USUARIOS REGISTRADOS",
             font=("Segoe UI", 16, "bold")).pack(pady=20)

    caja = tk.Text(win, width=50, height=12)
    caja.pack(pady=10)

    for u in obtener_todos_usuarios():
        caja.insert("end", f"Usuario: {u['usuario']}  |  Nombre: {u['nombre']}\n")

    tk.Button(win, text="Cerrar", command=win.destroy).pack(pady=10)