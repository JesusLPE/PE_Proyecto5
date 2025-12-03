import tkinter as tk
from tkinter import messagebox
from utilidades import cerrar_todo

import tkinter as tk
from tkinter import messagebox

def ventana_usuario(parent=None):
    user_win = tk.Toplevel(parent)
    user_win.title("Panel de Usuario - Boletería Ecuador")
    user_win.geometry("900x600")
    user_win.configure(bg="white")
    user_win.resizable(False, False)

    barra = tk.Frame(user_win, bg="#8B0000", height=60)
    barra.pack(fill="x")

    tk.Label(
        barra, text="Panel de Usuario - Boletería Ecuador",
        fg="white", bg="#8B0000",
        font=("Segoe UI", 20, "bold")
    ).pack(side="left", padx=20)

    tk.Button(
        barra, text="Cerrar",
        command=user_win.destroy,
        bg="white", fg="black", font=("Segoe UI", 12), width=10
    ).pack(side="right", padx=15, pady=10)

    cuerpo = tk.Frame(user_win, bg="white")
    cuerpo.pack(expand=True, pady=20)

    def crear_boton(texto, comando):
        return tk.Button(
            cuerpo, text=texto,
            font=("Segoe UI", 14, "bold"),
            width=25, height=2,
            bg="#B22222", fg="white",
            activebackground="#8B0000",
            activeforeground="white",
            bd=0, cursor="hand2",
            command=comando
        )

    def proximamente(nombre):
        messagebox.showinfo("Próximamente", f"La función '{nombre}' estará disponible próximamente.")

    funciones = [
        ("Comprar Boleto", lambda: proximamente("Comprar Boleto")),
        ("Ver Historial de Compras", lambda: proximamente("Historial de Compras")),
        ("Rutas Disponibles", lambda: proximamente("Rutas Disponibles")),
        ("Horarios de Viaje", lambda: proximamente("Horarios de Viaje")),
        ("Mis Boletos", lambda: proximamente("Mis Boletos")),
        ("Promociones Activas", lambda: proximamente("Promociones")),
        ("Métodos de Pago", lambda: proximamente("Métodos de Pago")),
        ("Editar Perfil", lambda: proximamente("Editar Perfil")),
        ("Notificaciones", lambda: proximamente("Notificaciones")),
        ("Viajes Programados", lambda: proximamente("Viajes Programados")),
    ]
    fila = 0
    col = 0

    for texto, comando in funciones:
        btn = crear_boton(texto, comando)
        btn.grid(row=fila, column=col, padx=25, pady=15)

        col += 1
        if col == 2:
            col = 0
            fila += 1